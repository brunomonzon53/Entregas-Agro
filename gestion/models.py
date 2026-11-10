from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Cliente(models.Model):
    razon_social = models.CharField(max_length=200)
    cuit = models.CharField(max_length=13, unique=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["razon_social"]

    def __str__(self):
        return self.razon_social


class CuentaCorriente(models.Model):

    class UnidadNegocio(models.TextChoices):
        FYO = "FYO", "FyO"
        CAMPO_SIMPLE = "CAMPO_SIMPLE", "Campo Simple"

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="cuentas"
    )

    unidad_negocio = models.CharField(
        max_length=20,
        choices=UnidadNegocio.choices
    )

    fecha_alta = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cuenta corriente"
        verbose_name_plural = "Cuentas corrientes"
        constraints = [
            models.UniqueConstraint(
                fields=["cliente", "unidad_negocio"],
                name="cuenta_unica_por_cliente_y_modulo"
            )
        ]

    def __str__(self):
        return f"{self.cliente} - {self.get_unidad_negocio_display()}"

    @property
    def saldo_actual(self):
        from django.db.models import Case, DecimalField, F, Sum, Value, When
        from django.db.models.functions import Coalesce

        resultado = self.movimientos.aggregate(
            saldo=Coalesce(
                Sum(
                    Case(
                        When(
                            tipo=Movimiento.TipoMovimiento.RETIRO,
                            then=-F("litros")
                        ),
                        default=F("litros"),
                        output_field=DecimalField(
                            max_digits=14,
                            decimal_places=2
                        )
                    )
                ),
                Value(0),
                output_field=DecimalField(
                    max_digits=14,
                    decimal_places=2
                )
            )
        )

        return resultado["saldo"]


class Movimiento(models.Model):

    class TipoMovimiento(models.TextChoices):
        LIQUIDACION = "LIQUIDACION", "Liquidación FyO"
        COMPRA = "COMPRA", "Compra Campo Simple"
        RETIRO = "RETIRO", "Retiro de combustible"

    class TipoLiquidacion(models.TextChoices):
        PARCIAL = "PARCIAL", "Parcial"
        FINAL = "FINAL", "Final"

    class TipoCombustible(models.TextChoices):
        SUPER = "SUPER", "Nafta Súper"
        PREMIUM = "PREMIUM", "Nafta Premium"
        DIESEL = "DIESEL", "Diésel"
        DIESEL_PREMIUM = "DIESEL_PREMIUM", "Diésel Premium"
        OTRO = "OTRO", "Otro"

    cuenta = models.ForeignKey(
        CuentaCorriente,
        on_delete=models.PROTECT,
        related_name="movimientos"
    )

    tipo = models.CharField(
        max_length=20,
        choices=TipoMovimiento.choices
    )

    fecha_operacion = models.DateField()

    litros = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        blank=True
    )

    combustible = models.CharField(
        max_length=20,
        choices=TipoCombustible.choices,
        blank=True
    )

    comprobante = models.CharField(
        max_length=100,
        blank=True
    )

    tipo_liquidacion = models.CharField(
        max_length=10,
        choices=TipoLiquidacion.choices,
        blank=True
    )

    importe = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True
    )

    precio_por_litro = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    observaciones = models.TextField(blank=True)

    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    fecha_carga = models.DateTimeField(auto_now_add=True)

    def clean(self):
        errores = {}

        if self.tipo in [
            self.TipoMovimiento.COMPRA,
            self.TipoMovimiento.RETIRO
        ]:
            if self.litros is None or self.litros <= 0:
                errores["litros"] = "Los litros deben ser mayores que cero."

        elif self.litros is not None and self.litros <= 0:
            errores["litros"] = "Los litros deben ser mayores que cero."

        if self.cuenta_id and self.tipo:
            unidad = self.cuenta.unidad_negocio

            if (
                self.tipo == self.TipoMovimiento.LIQUIDACION
                and unidad != CuentaCorriente.UnidadNegocio.FYO
            ):
                errores["tipo"] = "Las liquidaciones pertenecen únicamente a FyO."

            if (
                self.tipo == self.TipoMovimiento.COMPRA
                and unidad != CuentaCorriente.UnidadNegocio.CAMPO_SIMPLE
            ):
                errores["tipo"] = "Las compras pertenecen únicamente a Campo Simple."

            if (
                self.tipo == self.TipoMovimiento.LIQUIDACION
                and (self.importe is None or self.precio_por_litro is None)
            ):
                errores["importe"] = "La liquidación requiere importe y precio por litro."

            if (
                self.tipo == self.TipoMovimiento.LIQUIDACION
                and self.importe is not None
                and self.precio_por_litro is not None
            ):
                if self.importe <= 0 or self.precio_por_litro <= 0:
                    errores["importe"] = "El importe y el precio deben ser mayores que cero."

            if (
                self.tipo == self.TipoMovimiento.LIQUIDACION
                and not self.tipo_liquidacion
            ):
                errores["tipo_liquidacion"] = "Indicá si la liquidación es parcial o final."

            if (
                self.tipo in [
                    self.TipoMovimiento.COMPRA,
                    self.TipoMovimiento.RETIRO
                ]
                and not self.combustible
            ):
                errores["combustible"] = "Debés indicar el tipo de combustible."

        if errores:
            raise ValidationError(errores)

    def save(self, *args, **kwargs):
        if (
            self.tipo == self.TipoMovimiento.LIQUIDACION
            and self.importe is not None
            and self.precio_por_litro is not None
            and self.precio_por_litro > 0
        ):
            self.litros = (
                self.importe / self.precio_por_litro
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"
        ordering = ["-fecha_operacion", "-fecha_carga"]

    def __str__(self):
        return (
            f"{self.cuenta} - {self.get_tipo_display()} "
            f"- {self.litros} litros"
        )