
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path("clientes/", views.lista_clientes, name="lista_clientes"),
    path("clientes/<int:cliente_id>/", views.detalle_cliente, name="detalle_cliente"),

    path("movimientos/", views.lista_movimientos, name="lista_movimientos"),

    path(
        "movimientos/nueva-liquidacion-fyo/",
        views.crear_liquidacion_fyo,
        name="crear_liquidacion_fyo"
    ),
    path(
        "movimientos/nueva-compra-campo-simple/",
        views.crear_compra_campo_simple,
        name="crear_compra_campo_simple"
    ),
    path(
        "movimientos/nuevo-retiro/",
        views.crear_retiro,
        name="crear_retiro"
    ),
    path(
        "cuentas-corrientes/",
        views.lista_cuentas_corrientes,
        name="lista_cuentas_corrientes"
    ),
    path("asistente/", views.chatbot, name="chatbot"),
]
