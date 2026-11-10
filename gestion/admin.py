from django.contrib import admin
from .models import Cliente, CuentaCorriente, Movimiento


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("razon_social", "cuit", "fecha_alta")
    search_fields = ("razon_social", "cuit")


@admin.register(CuentaCorriente)
class CuentaCorrienteAdmin(admin.ModelAdmin):
    list_display = (
        "cliente",
        "unidad_negocio",
        "saldo",
        "fecha_alta",
    )
    list_filter = ("unidad_negocio",)
    search_fields = ("cliente__razon_social", "cliente__cuit")

    @admin.display(description="Saldo actual (litros)")
    def saldo(self, obj):
        return f"{obj.saldo_actual:,.2f}"


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_operacion",
        "cuenta",
        "tipo",
        "litros",
        "combustible",
        "comprobante",
        "registrado_por",
        "fecha_carga",
    )

    list_filter = (
        "tipo",
        "cuenta__unidad_negocio",
        "combustible",
        "fecha_operacion",
    )

    search_fields = (
        "cuenta__cliente__razon_social",
        "comprobante",
    )

    readonly_fields = (
        "registrado_por",
        "fecha_carga",
    )

    def save_model(self, request, obj, form, change):
        if not change and not obj.registrado_por_id:
            obj.registrado_por = request.user

        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False
