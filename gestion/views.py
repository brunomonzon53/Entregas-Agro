from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    LiquidacionFyOForm,
    CompraCampoSimpleForm,
    RetiroForm,
)
from .models import Cliente, CuentaCorriente, Movimiento
from django.db.models import Q

@login_required
def dashboard(request):

    clientes = Cliente.objects.count()
    cuentas = CuentaCorriente.objects.count()
    movimientos = Movimiento.objects.count()

    cuentas_fyo = CuentaCorriente.objects.filter(
        unidad_negocio="FYO"
    )

    cuentas_campo = CuentaCorriente.objects.filter(
        unidad_negocio="CAMPO_SIMPLE"
    )

    saldo_fyo = sum(
        (cuenta.saldo_actual for cuenta in cuentas_fyo),
        start=0
    )

    saldo_campo = sum(
        (cuenta.saldo_actual for cuenta in cuentas_campo),
        start=0
    )

    ultimos_movimientos = Movimiento.objects.select_related(
        "cuenta",
        "cuenta__cliente"
    )[:8]

    contexto = {
        "clientes": clientes,
        "cuentas": cuentas,
        "movimientos": movimientos,
        "saldo_fyo": saldo_fyo,
        "saldo_campo": saldo_campo,
        "ultimos_movimientos": ultimos_movimientos,
    }

    return render(request, "gestion/dashboard.html", contexto)


@login_required
def lista_clientes(request):
    busqueda = request.GET.get("buscar", "")
    clientes = Cliente.objects.all()

    if busqueda:
        clientes = clientes.filter(
            Q(razon_social__icontains=busqueda) |
            Q(cuit__icontains=busqueda)
        )

    contexto = {
        "clientes": clientes,
        "busqueda": busqueda,
    }

    return render(request, "gestion/clientes.html", contexto)


@login_required
def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    cuentas = CuentaCorriente.objects.filter(cliente=cliente)

    movimientos = Movimiento.objects.filter(
        cuenta__cliente=cliente
    ).select_related(
        "cuenta",
        "cuenta__cliente"
    ).order_by("-fecha_operacion", "-fecha_carga")

    contexto = {
        "cliente": cliente,
        "cuentas": cuentas,
        "movimientos": movimientos,
    }

    return render(request, "gestion/detalle_cliente.html", contexto)


@login_required
def lista_movimientos(request):

    busqueda = request.GET.get("buscar", "")
    unidad = request.GET.get("unidad", "")
    tipo = request.GET.get("tipo", "")

    movimientos = Movimiento.objects.select_related(
        "cuenta",
        "cuenta__cliente"
    )

    if busqueda:
        movimientos = movimientos.filter(
            Q(cuenta__cliente__razon_social__icontains=busqueda) |
            Q(cuenta__cliente__cuit__icontains=busqueda) |
            Q(comprobante__icontains=busqueda)
        )

    if unidad:
        movimientos = movimientos.filter(
            cuenta__unidad_negocio=unidad
        )

    if tipo:
        movimientos = movimientos.filter(
            tipo=tipo
        )

    movimientos = movimientos.order_by(
        "-fecha_operacion",
        "-fecha_carga"
    )

    contexto = {
        "movimientos": movimientos,
        "busqueda": busqueda,
        "unidad": unidad,
        "tipo": tipo,
        "unidades": CuentaCorriente.UnidadNegocio.choices,
        "tipos": Movimiento.TipoMovimiento.choices,
    }

    return render(
        request,
        "gestion/movimientos.html",
        contexto
    )


@login_required
def crear_liquidacion_fyo(request):

    if request.method == "POST":
        formulario = LiquidacionFyOForm(request.POST)

        if formulario.is_valid():
            movimiento = formulario.save(commit=False)
            movimiento.registrado_por = request.user
            movimiento.save()

            return redirect("lista_movimientos")

    else:
        formulario = LiquidacionFyOForm()

    contexto = {
        "formulario": formulario,
    }

    return render(
        request,
        "gestion/crear_liquidacion_final.html",
        contexto
    )


@login_required
def crear_compra_campo_simple(request):

    if request.method == "POST":
        form = CompraCampoSimpleForm(request.POST)

        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.registrado_por = request.user
            movimiento.save()

            return redirect("lista_movimientos")

    else:
        form = CompraCampoSimpleForm()

    return render(
        request,
        "gestion/crear_compra_campo_simple.html",
        {"form": form}
    )


@login_required
def crear_retiro(request):

    if request.method == "POST":
        form = RetiroForm(request.POST)

        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.registrado_por = request.user
            movimiento.save()

            return redirect("lista_movimientos")

    else:
        form = RetiroForm()

    return render(
        request,
        "gestion/crear_retiro.html",
        {"form": form}
    )


@login_required
def lista_cuentas_corrientes(request):

    cuentas = (
        CuentaCorriente.objects
        .select_related("cliente")
        .order_by(
            "unidad_negocio",
            "cliente__razon_social"
        )
    )

    return render(
        request,
        "gestion/cuentas_corrientes.html",
        {"cuentas": cuentas}
    )


@login_required
def chatbot(request):
    return render(request, "gestion/chatbot.html")
