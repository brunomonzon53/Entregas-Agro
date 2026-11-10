from django import forms

from .models import CuentaCorriente, Movimiento


class LiquidacionFyOForm(forms.ModelForm):

    class Meta:
        model = Movimiento

        fields = [
            "cuenta",
            "fecha_operacion",
            "importe",
            "precio_por_litro",
            "tipo_liquidacion",
            "comprobante",
            "observaciones",
        ]

        labels = {
            "cuenta": "Cliente / Cuenta FyO",
            "fecha_operacion": "Fecha de operación",
            "importe": "Importe de liquidación ($)",
            "precio_por_litro": "Precio por litro ($)",
            "tipo_liquidacion": "Tipo de liquidación",
            "comprobante": "Número de comprobante",
            "observaciones": "Observaciones",
        }

        widgets = {
            "fecha_operacion": forms.DateInput(
                attrs={"type": "date"}
            ),

            "importe": forms.NumberInput(
                attrs={"placeholder": "Ej. 5000000", "step": "0.01", "min": "0.01"}
            ),

            "precio_por_litro": forms.NumberInput(
                attrs={"placeholder": "Ej. 1000", "step": "0.01", "min": "0.01"}
            ),

            "comprobante": forms.TextInput(
                attrs={"placeholder": "Número de comprobante"}
            ),

            "observaciones": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Observaciones adicionales"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["cuenta"].queryset = (
            CuentaCorriente.objects
            .filter(
                unidad_negocio=CuentaCorriente.UnidadNegocio.FYO
            )
            .select_related("cliente")
            .order_by("cliente__razon_social")
        )

    def save(self, commit=True):
        movimiento = super().save(commit=False)

        movimiento.tipo = Movimiento.TipoMovimiento.LIQUIDACION

        if commit:
            movimiento.save()

        return movimiento


class CompraCampoSimpleForm(forms.ModelForm):

    class Meta:
        model = Movimiento

        fields = [
            "cuenta",
            "fecha_operacion",
            "litros",
            "combustible",
            "comprobante",
            "observaciones",
        ]

        labels = {
            "cuenta": "Cliente / Cuenta Campo Simple",
            "fecha_operacion": "Fecha de operación",
            "litros": "Cantidad de litros",
            "combustible": "Tipo de combustible",
            "comprobante": "Número de comprobante",
            "observaciones": "Observaciones",
        }

        widgets = {
            "fecha_operacion": forms.DateInput(
                attrs={"type": "date"}
            ),

            "litros": forms.NumberInput(
                attrs={
                    "placeholder": "Ej. 5000",
                    "step": "0.01",
                    "min": "0.01"
                }
            ),

            "comprobante": forms.TextInput(
                attrs={"placeholder": "Número de comprobante"}
            ),

            "observaciones": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Observaciones adicionales"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["cuenta"].queryset = (
            CuentaCorriente.objects
            .filter(
                unidad_negocio=CuentaCorriente.UnidadNegocio.CAMPO_SIMPLE
            )
            .select_related("cliente")
            .order_by("cliente__razon_social")
        )

    def save(self, commit=True):
        movimiento = super().save(commit=False)

        movimiento.tipo = Movimiento.TipoMovimiento.COMPRA

        if commit:
            movimiento.save()

        return movimiento


class RetiroForm(forms.ModelForm):

    class Meta:
        model = Movimiento

        fields = [
            "cuenta",
            "fecha_operacion",
            "litros",
            "combustible",
            "comprobante",
            "observaciones",
        ]

        labels = {
            "cuenta": "Cliente / Cuenta corriente",
            "fecha_operacion": "Fecha del retiro",
            "litros": "Cantidad de litros a retirar",
            "combustible": "Tipo de combustible",
            "comprobante": "Número de remito",
            "observaciones": "Observaciones",
        }

        widgets = {
            "fecha_operacion": forms.DateInput(
                attrs={"type": "date"}
            ),

            "litros": forms.NumberInput(
                attrs={
                    "placeholder": "Ej. 1000",
                    "step": "0.01",
                    "min": "0.01"
                }
            ),

            "comprobante": forms.TextInput(
                attrs={"placeholder": "Número de remito"}
            ),

            "observaciones": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Observaciones adicionales"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["cuenta"].queryset = (
            CuentaCorriente.objects
            .select_related("cliente")
            .order_by(
                "cliente__razon_social",
                "unidad_negocio"
            )
        )

    def save(self, commit=True):
        movimiento = super().save(commit=False)

        movimiento.tipo = Movimiento.TipoMovimiento.RETIRO

        if commit:
            movimiento.save()

        return movimiento
