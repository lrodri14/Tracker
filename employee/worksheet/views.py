# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

from datetime import date, datetime
from dateutil import relativedelta
from decimal import *
from django.db.models import Q,Count, Min, Sum, Avg, OuterRef, Subquery
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core import serializers
from django.core.mail import EmailMultiAlternatives
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import Context
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views.generic import View
from email.mime.image import MIMEImage
from io import BytesIO
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from xhtml2pdf import pisa
from .forms import *
from .models import *
from .render import Render
import datetime as dtiempo
import functools
import json
import locale
import operator
import pandas
import uuid
import xlsxwriter

locale.setlocale(locale.LC_ALL, "")
TWOPLACES = Decimal(10) ** -2

# Create your views here.


def verificaSucursal(request):
    if not "sucursal" in request.session:
        return HttpResponseRedirect("/salir/")
    else:
        if int(request.session["sucursal"]) < 1:
            return HttpResponseRedirect("/salir/")


@login_required(login_url="/form/iniciar-sesion/")
def home(request):
    if not "sucursal" in request.session:
        return HttpResponseRedirect("/salir/")
    else:
        if int(request.session["sucursal"]) < 1:
            return HttpResponseRedirect("/salir/")
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(branch=suc).values(
        "id", "firstName", "middleName", "lastName"
    )
    return render(request, "index.html", {"empleados": empleados})


def inicia_sesion(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    return render(request, "iniciar-sesion.html")


def ingresar(request):
    Sucursales = None

    if not request.user.is_anonymous():
        return HttpResponseRedirect("/")

    # if "next" in request.GET:
    #     if not request.GET._mutable:
    #         request.GET._mutable = True
    #         request.GET["next"] = request.GET.get["next"]
    # else:
    #     print("No existe variable en request")

    if request.method == "POST":
        frmSesion = AuthenticationForm(request.POST)
        usuario = request.POST["username"]
        clave = request.POST["password"]
        acceso = authenticate(username=usuario, password=clave)

        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                totReg = UsuarioSucursal.objects.filter(
                    usuario=request.user, active=True
                ).count()
                if totReg > 0:
                    if totReg > 1:
                        return HttpResponseRedirect("/seleccionar/sucursal/")
                    else:
                        sucursal = UsuarioSucursal.objects.get(
                            usuario=request.user, active=True
                        )
                        request.session[
                            "nombre_sucursal"
                        ] = sucursal.sucursal.description
                        request.session["sucursal"] = sucursal.sucursal.pk
                        return HttpResponseRedirect("/")
                else:
                    return HttpResponseRedirect("/salir/")
            else:
                return render(request, "no-activo.html")
        else:
            return render(request, "no-usuario.html")
    else:
        frmSesion = AuthenticationForm()
        return HttpResponseRedirect("/form/iniciar-sesion/")


@login_required(login_url="/form/iniciar-sesion/")
def seleccionar_sucursal(request):
    empresas = []
    empresa = {}
    if "next" in request.GET:
        if not request.GET._mutable:
            request.GET._mutable = True
            request.GET["next"] = request.GET.get["next"]
    sucursales = UsuarioSucursal.objects.filter(usuario=request.user)
    empresa_flat = (
        UsuarioSucursal.objects.filter(usuario=request.user)
        .values_list("sucursal__empresa_id", flat=True)
        .distinct()
    )
    empresas = Empresa.objects.filter(pk__in=empresa_flat)
    return render(
        request,
        "seleccionar_sucursal.html",
        {"sucursales": sucursales, "empresas": empresas},
    )


def recibir_sucursal(request):
    if request.method == "POST":
        IdSucursal = request.POST["sucursal"]
        totreg = Branch.objects.filter(pk=IdSucursal).count()
        if totreg > 0:
            sucursal = Branch.objects.get(pk=IdSucursal)
            request.session["nombre_sucursal"] = sucursal.description
            request.session["sucursal"] = IdSucursal
            return HttpResponseRedirect("/")
        else:
            request.session["sucursal"] = 0
            request.session["nombre_sucursal"] = ""
            return HttpResponseRedirect("/seleccionar/sucursal/")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_employee", raise_exception=True)
def empleado_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])

    verificaSucursal(request)
    # Position.objects.filter(active=True, empresa_reg=suc.empresa)
    positions = []
    departments = Department.objects.filter(active=True, empresa_reg=suc.empresa)
    branches = Branch.objects.filter(active=True)
    salesPersons = Vendedor.objects.filter(active=True, empresa_reg=suc.empresa)
    states = State.objects.filter(active=True, empresa_reg=suc.empresa)
    countries = Country.objects.filter(active=True, empresa_reg=suc.empresa)
    estados_emp = StatusEmp.objects.filter(active=True, empresa_reg=suc.empresa)
    terms = TermReason.objects.filter(active=True, empresa_reg=suc.empresa)
    sexos = Sex.objects.filter(active=True, empresa_reg=suc.empresa)
    citizenships = Country.objects.filter(active=True, empresa_reg=suc.empresa)
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    civil_status = CivilStatus.objects.filter(active=True)
    salary_units = SalaryUnit.objects.filter(active=True, empresa_reg=suc.empresa)
    costs_units = CostUnit.objects.filter(active=True, empresa_reg=suc.empresa)
    banks = Bank.objects.filter(active=True)
    tipos_contratos = TipoContrato.objects.filter(active=True, empresa_reg=suc.empresa)
    tipos_nominas = TipoNomina.objects.filter(active=True, empresa_reg=suc.empresa)
    funciones_operativas = FuncionesTrabajo.objects.filter(
        active=True, empresa_reg=suc.empresa
    )
    return render(
        request,
        "empleado-form.html",
        {
            "banks": banks,
            "costs_units": costs_units,
            "salary_units": salary_units,
            "civil_status": civil_status,
            "citizenships": citizenships,
            "positions": positions,
            "departments": departments,
            "branches": branches,
            "salesPersons": salesPersons,
            "states": states,
            "countries": countries,
            "stats": estados_emp,
            "terms": terms,
            "sexs": sexos,
            "empleados": empleados,
            "tipos_contratos": tipos_contratos,
            "tipos_nominas": tipos_nominas,
            "funciones_operativas": funciones_operativas,
        },
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_employee", raise_exception=True)
def empleado_editar(request, id):
    antiguedad = None
    suc = Branch.objects.get(pk=request.session["sucursal"])

    dato = Employee.objects.get(pk=id)

    positions = Position.objects.filter(active=True, empresa_reg=suc.empresa)
    departments = Department.objects.filter(active=True, empresa_reg=suc.empresa)
    branches = Branch.objects.filter(active=True)
    salesPersons = Vendedor.objects.filter(active=True, empresa_reg=suc.empresa)
    states = State.objects.filter(active=True, empresa_reg=suc.empresa)
    countries = Country.objects.filter(active=True, empresa_reg=suc.empresa)
    estados_emp = StatusEmp.objects.filter(active=True, empresa_reg=suc.empresa)
    terms = TermReason.objects.filter(active=True, empresa_reg=suc.empresa)
    sexos = Sex.objects.filter(active=True, empresa_reg=suc.empresa)
    citizenships = Country.objects.filter(active=True, empresa_reg=suc.empresa)
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    civil_status = CivilStatus.objects.filter(active=True, empresa_reg=suc.empresa)
    salary_units = SalaryUnit.objects.filter(active=True, empresa_reg=suc.empresa)

    costs_units = CostUnit.objects.filter(active=True, empresa_reg=suc.empresa)
    banks = Bank.objects.filter(active=True, empresa_reg=suc.empresa)
    tipos_contratos = TipoContrato.objects.filter(active=True, empresa_reg=suc.empresa)
    tipos_nominas = TipoNomina.objects.filter(active=True, empresa_reg=suc.empresa)
    if dato.active:
        rd = relativedelta.relativedelta(date.today(), dato.startDate)
    else:
        rd = relativedelta.relativedelta(dato.termDate, dato.startDate)
    antiguedad = "{0.years} años, {0.months} meses y {0.days} días".format(rd)
    funciones_operativas = FuncionesTrabajo.objects.filter(
        active=True, empresa_reg=suc.empresa
    )
    return render(
        request,
        "empleado-form.html",
        {
            "editar": True,
            "dato": dato,
            "banks": banks,
            "costs_units": costs_units,
            "salary_units": salary_units,
            "civil_status": civil_status,
            "citizenships": citizenships,
            "positions": positions,
            "departments": departments,
            "branches": branches,
            "salesPersons": salesPersons,
            "states": states,
            "countries": countries,
            "stats": estados_emp,
            "terms": terms,
            "sexs": sexos,
            "empleados": empleados,
            "tipos_contratos": tipos_contratos,
            "tipos_nominas": tipos_nominas,
            "funciones_operativas": funciones_operativas,
            "antiguedad": antiguedad,
        },
    )
    # return render(request, 'empleado-form.html', {'editar':True, 'dato':dato, 'positions':positions, 'departments':departments, 'branches':branches, 'salesPersons':salesPersons})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_employee", raise_exception=True)
def empleado_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(branch=suc)
    return render(request, "empleado-listado.html", {"empleados": empleados})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_reg_employee", raise_exception=True)
def empleado_perfil(request, id):
    periodos_pago = 0
    periodos = []
    l_datos = []
    l_pagos = []
    deducciones_legales = [
        {"deduccion": "IHSS", "descripcion": "I.H.S.S"},
        {"deduccion": "RAP", "descripcion": "R.A.P."},
        {"deduccion": "ISR", "descripcion": "Impuesto sobre renta"},
        {"deduccion": "IMV", "descripcion": "Impuesto Vecinal"},
    ]
    dato = Employee.objects.get(pk=id)
    if dato:
        if dato.salaryUnits:
            if dato.salaryUnits.dias_salario:
                periodos_pago = 30 / dato.salaryUnits.dias_salario
                for i in range(0, int(periodos_pago)):
                    i += 1
                    periodos.append(i)
    tot_reg = ImagenEmpleado.objects.filter(empleado__id=id).count()
    if tot_reg > 0:
        imagen = ImagenEmpleado.objects.get(empleado__id=id)
    else:
        imagen = None
    if dato.active:
        rd = relativedelta.relativedelta(date.today(), dato.startDate)
    else:
        rd = relativedelta.relativedelta(dato.termDate, dato.startDate)
    antiguedad = "{0.years} años, {0.months} meses y {0.days} días".format(rd)
    planillas = (
        PlanillaDetalle.objects.select_related("planilla")
        .filter(empleado=dato, planilla__cerrada=True)
        .values("planilla__id", "planilla__descripcion")
    )
    lista1 = DeduccionIndividualSubDetalle.objects.filter(
        deduccion__empleado=dato
    )
    for item in lista1:
        l_pagos = []
        v_suma_ = 0
        # pagos = ControlPagosDeduccionIndividual.objects.filter(
        #     deduccion=item.deduccion
        # )

        # for pago in pagos:
        #     o_pago = {
        #         "planilla": pago.planilla,
        #         "deduccion": pago.deduccion,
        #         "valor": formato_millar(pago.valor),
        #     }
        #     l_pagos.append(o_pago)

        # suma_v = ControlPagosDeduccionIndividual.objects.filter(
        #     deduccion=item.deducciondetalle
        # ).aggregate(Sum("valor"))
        # if suma_v["valor__sum"]:
        #     v_suma_ = suma_v["valor__sum"]
        # print(suma_v)
        objeto = {
            "id": item.pk,
            "descripcion": item.descripcion,
            "monto": formato_millar(item.monto),
            "deduccion": item.deduccion,
            "detalle_pagos": l_pagos,
            "total_pagado": formato_millar(v_suma_),
        }

        l_datos.append(objeto)
    return render(
        request,
        "perfil-empleado.html",
        {
            "dato": dato,
            "imagen": imagen,
            "periodos": periodos,
            "deducciones_legales": deducciones_legales,
            "antiguedad": antiguedad,
            "planillas": planillas,
            "control_saldo": l_datos,
        },
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_grupocorporativo", raise_exception=True)
def corporativo(request):
    return render(request, "corporativo.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_grupocorporativo", raise_exception=True)
def corporativo_editar(request, reg_id):
    dato = GrupoCorporativo.objects.get(pk=reg_id)
    return render(request, "corporativo.html", {"dato": dato, "editar": True})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_grupocorporativo", raise_exception=True)
def listadoCorporativo(request):
    listado = None

    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_empresa"):
        listado = GrupoCorporativo.objects.filter(
            razonSocial=suc.empresa.grupo.razonSocial
        ).order_by("date_reg")
    else:
        if request.user.has_perm("worksheet.see_empresa"):
            listado = GrupoCorporativo.objects.filter(
                active=True, razonSocial=suc.empresa.grupo.razonSocial
            ).order_by("date_reg")
    return render(request, "corporativo-listado.html", {"corporativos": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_empresa", raise_exception=True)
def empresa(request):
    return render(request, "empresa.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_empresa", raise_exception=True)
def empresa_editar(request, emp_id):
    dato = Empresa.objects.get(pk=emp_id)
    return render(request, "empresa.html", {"dato": dato, "editar": True})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_empresa", raise_exception=True)
def listadoEmpresa(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_empresa"):
        listado = empresas = Empresa.objects.filter(grupo=suc.empresa.grupo)
    else:
        if request.user.has_perm("worksheet.see_empresa"):
            listado = empresas = Empresa.objects.filter(
                active=True, grupo=suc.empresa.grupo
            )
    return render(request, "empresa-listado.html", {"empresas": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_branch", raise_exception=True)
def sucursal(request):
    return render(request, "sucursal.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_branch", raise_exception=True)
def sucursal_editar(request, id):
    dato = Branch.objects.get(pk=id)
    return render(request, "sucursal.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_branch", raise_exception=True)
def listadoSucursal(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_branch"):
        listado = Branch.objects.filter(empresa=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_branch"):
            listado = Branch.objects.filter(active=True, empresa=suc.empresa)
    return render(request, "sucursal-listado.html", {"sucursales": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_divisiones", raise_exception=True)
def divisiones(request):
    return render(request, "divisiones.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_divisiones", raise_exception=True)
def division_editar(request, id):
    dato = Divisiones.objects.get(pk=id)
    return render(request, "divisiones.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_divisiones", raise_exception=True)
def listadoDivisiones(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_divisiones"):
        listado = Divisiones.objects.filter(empresa_reg=suc.empresa)
    else:

        if request.user.has_perm("worksheet.see_divisiones"):
            listado = Divisiones.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "divisiones-listado.html", {"divisiones": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_department", raise_exception=True)
def departamentos(request):
    return render(request, "departamentos.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_department", raise_exception=True)
def departamento_editar(request, id):
    dato = Department.objects.get(pk=id)
    return render(request, "departamentos.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_department", raise_exception=True)
def listadoDepartamentos(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_department"):
        listado = Department.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_department"):
            listado = Department.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "departamento-listado.html", {"deptos": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_position", raise_exception=True)
def puestoTrabajo(request):
    verificaSucursal(request)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    funciones_operativas = FuncionesTrabajo.objects.filter(
        empresa_reg=suc.empresa, active=True
    )
    return render(
        request, "puesto-trabajo.html", {"funciones_operativas": funciones_operativas}
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_position", raise_exception=True)
def puesto_editar(request, id):
    verificaSucursal(request)
    dato = Position.objects.get(pk=id)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    funciones_operativas = FuncionesTrabajo.objects.filter(
        empresa_reg=suc.empresa, active=True
    )
    return render(
        request,
        "puesto-trabajo.html",
        {"editar": True, "dato": dato, "funciones_operativas": funciones_operativas},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_position", raise_exception=True)
def listadoPuestoTrabajo(request):
    listado = []
    verificaSucursal(request)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_position"):
        listado = Position.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_position"):
            listado = Position.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "puestos-listado.html", {"puesto": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_centroscostos", raise_exception=True)
def centro_costos(request):
    return render(request, "centro-costos.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_centroscostos", raise_exception=True)
def centro_costo_editar(request, id):
    dato = CentrosCostos.objects.get(pk=id)
    return render(request, "centro-costos.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_centroscostos", raise_exception=True)
def listadoCentroCostos(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_centroscostos"):
        listado = CentrosCostos.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_centroscostos"):
            listado = CentrosCostos.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "ccostos-listado.html", {"ccostos": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_country", raise_exception=True)
def paises(request):
    return render(request, "paises.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_country", raise_exception=True)
def paises_editar(request, id):
    dato = Country.objects.get(pk=id)
    return render(request, "paises.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_country", raise_exception=True)
def listadoPaises(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_country") or request.user.is_superuser:
        listado = Country.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_country"):
            listado = Country.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "paises-listado.html", {"paises": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_state", raise_exception=True)
def deptos_pais(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    paises = Country.objects.filter(empresa_reg=suc.empresa)
    return render(request, "deptos-pais.html", {"paises": paises})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_state", raise_exception=True)
def deptos_pais_editar(request, id):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    dato = State.objects.get(pk=id)
    paises = Country.objects.filter(empresa_reg=suc.empresa)
    return render(
        request, "deptos-pais.html", {"editar": True, "dato": dato, "paises": paises}
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_state", raise_exception=True)
def deptos_pais_listado(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_state"):
        listado = State.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_state"):
            listado = State.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "deptos-pais-listado.html", {"deptos": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_ciudad", raise_exception=True)
def ciudad(request):
    return render(request, "ciudad.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_ciudad", raise_exception=True)
def ciudad_editar(request, id):
    dato = Ciudad.objects.get(pk=id)
    return render(request, "ciudad.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_ciudad", raise_exception=True)
def ciudades_listado(request):
    listado = []
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_ciudad"):
        listado = Ciudad.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_ciudad"):
            listado = Ciudad.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "ciudades-listado.html", {"ciudades": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_sex", raise_exception=True)
def genero(request):
    return render(request, "genero.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_sex", raise_exception=True)
def genero_editar(request, id):
    dato = Sex.objects.get(pk=id)
    return render(request, "genero.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_sex", raise_exception=True)
def generos_listado(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_sex"):
        listado = Sex.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_sex"):
            listado = Sex.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "genero-listado.html", {"generos": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_civilstatus", raise_exception=True)
def estado_civil(request):
    return render(request, "estado-civil.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_civilstatus", raise_exception=True)
def estado_civil_editar(request, id):
    dato = CivilStatus.objects.get(pk=id)
    return render(request, "estado-civil.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_civilstatus", raise_exception=True)
def estado_civil_listado(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_civilstatus"):
        listado = CivilStatus.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_civilstatus"):
            listado = CivilStatus.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "estado-civil-listado.html", {"estados": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_parentesco", raise_exception=True)
def parentesco(request):
    return render(request, "parentesco.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_parentesco", raise_exception=True)
def parentesco_editar(request, id):
    dato = Parentesco.objects.get(pk=id)
    return render(request, "parentesco.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_parentesco", raise_exception=True)
def parentesco_listado(request):
    listado = []
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_parentesco"):
        listado = Parentesco.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_parentesco"):
            listado = Parentesco.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "parentesco-listado.html", {"parentescos": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_funcionestrabajo", raise_exception=True)
def funcion_trabajo(request):
    return render(request, "funciones-trabajo.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_funcionestrabajo", raise_exception=True)
def funcion_trabajo_editar(request, id):
    funcion = FuncionesTrabajo.objects.get(pk=id)
    return render(request, "funciones-trabajo.html", {"dato": funcion, "editar": True})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_funcionestrabajo", raise_exception=True)
def funcion_trab_listado(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_funcionestrabajo"):
        listado = FuncionesTrabajo.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_funcionestrabajo"):
            listado = FuncionesTrabajo.objects.filter(
                active=True, empresa_reg=suc.empresa
            )
    return render(request, "funciones-trabajo-listado.html", {"funciones": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_equipotrabajo", raise_exception=True)
def equipo_trabajo(request):
    return render(request, "equipo-trabajo.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_equipotrabajo", raise_exception=True)
def equipo_trabajo_editar(request, id):
    dato = EquipoTrabajo.objects.get(pk=id)
    return render(request, "equipo-trabajo.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_equipotrabajo", raise_exception=True)
def equipo_trabajo_listado(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_equipotrabajo"):
        listado = EquipoTrabajo.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_equipotrabajo"):
            listado = EquipoTrabajo.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "equipo-trabajo-listado.html", {"equipos": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_statusemp", raise_exception=True)
def estado_empleado(request):
    return render(request, "estatus-empleado.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_statusemp", raise_exception=True)
def estado_empleado_editar(request, id):
    dato = StatusEmp.objects.get(pk=id)
    return render(request, "estatus-empleado.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_statusemp", raise_exception=True)
def estado_empleado_listado(request):
    listado = []
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_statusemp"):
        listado = StatusEmp.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_statusemp"):
            listado = StatusEmp.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "estado-empleado-listado.html", {"lista": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_ausentismo", raise_exception=True)
def ausentismo(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, branch=suc).order_by("firstName")
    motivos = MotivosAusencia.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(
        request, "ausentismo.html", {"empleados": empleados, "motivos": motivos}
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_ausentismo", raise_exception=True)
def ausentismo_editar(request, id):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    dato = Ausentismo.objects.get(pk=id)
    motivos = MotivosAusencia.objects.filter(active=True, empresa_reg=suc.empresa)
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(
        request,
        "ausentismo.html",
        {"editar": True, "dato": dato, "empleados": empleados, "motivos": motivos},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_ausentismo", raise_exception=True)
def ausentismo_listado(request):
    lista = []
    listado = None
    busqueda = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, branch=suc).order_by("firstName")
    if "empleado" in request.GET:
        emp = request.GET.get("empleado")
        if len(emp) > 0:
            if int(emp) > 0:
                busqueda = int(emp)
                empleado = Employee.objects.get(pk=busqueda)
                if request.user.has_perm("worksheet.see_all_ausentismo"):
                    listado = Ausentismo.objects.filter(
                        pk=busqueda, empresa_reg=suc.empresa
                    ).order_by('-desde')
                else:
                    if request.user.has_perm("worksheet.see_ausentismo"):
                        listado = Ausentismo.objects.filter(
                            pk=busqueda, active=True, empresa_reg=suc.empresa
                        ).order_by('-desde')
            else:
                lista = Ausentismo.objects.filter(sucursal_reg=suc).order_by('-desde')
        else:
            lista = Ausentismo.objects.filter(sucursal_reg=suc).order_by('-desde')
    else:
        lista = Ausentismo.objects.filter(sucursal_reg=suc).order_by('-desde')
    # lista = Ausentismo.objects.all().order_by('-desde')
    # empleados = Employee.objects.filter(empresa_reg=suc.empresa)
    return render(
        request,
        "ausentismo-listado.html",
        {"datos": lista, "empleados": empleados, "busqueda": busqueda},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_motivosausencia", raise_exception=True)
def motivos_ausencia(request):
    return render(request, "motivos-ausencia.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_motivosausencia", raise_exception=True)
def motivos_ausencia_editar(request, id):
    dato = MotivosAusencia.objects.get(pk=id)
    return render(request, "motivos-ausencia.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_motivosausencia", raise_exception=True)
def motivos_ausencia_listado(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_motivosausencia"):
        listado = MotivosAusencia.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_motivosausencia"):
            listado = MotivosAusencia.objects.filter(
                active=True, empresa_reg=suc.empresa
            )
    return render(request, "motivos-ausencia-listado.html", {"lista": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_motivosdespido", raise_exception=True)
def motivo_despido(request):
    return render(request, "motivos-despido.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_motivosdespido", raise_exception=True)
def motivo_despido_editar(request, id):
    dato = MotivosDespido.objects.get(pk=id)
    return render(request, "motivos-despido.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_motivosdespido", raise_exception=True)
def motivos_despido_listado(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_motivosdespido"):
        listado = MotivosDespido.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_motivosdespido"):
            listado = MotivosDespido.objects.filter(
                active=True, empresa_reg=suc.empresa
            )
    return render(request, "motivos-despido-listado.html", {"lista": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_motivosrenuncia", raise_exception=True)
def motivos_renuncia(request):
    return render(request, "motivos-renuncia.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_motivosrenuncia", raise_exception=True)
def motivos_renuncia_editar(request, id):
    dato = MotivosRenuncia.objects.get(pk=id)
    return render(request, "motivos-renuncia.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_motivosrenuncia", raise_exception=True)
def motivos_renuncia_listado(request):
    listado = []
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_motivosrenuncia"):
        listado = MotivosRenuncia.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_motivosrenuncia"):
            listado = MotivosRenuncia.objects.filter(
                active=True, empresa_reg=suc.empresa
            )
    return render(request, "motivos-renuncia-listado.html", {"lista": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_claseeducacion", raise_exception=True)
def clase_educacion(request):
    return render(request, "clase-educacion.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_calseeducacion", raise_exception=True)
def clase_educacion_editar(request, id):
    dato = ClaseEducacion.objects.get(pk=id)
    return render(request, "clase-educacion.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_claseeduacion", raise_exception=True)
def clase_educacion_listado(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_claseeducacion"):
        listado = ClaseEducacion.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_claseeducacion"):
            listado = ClaseEducacion.objects.filter(
                active=True, empresa_reg=suc.empresa
            )
    return render(request, "clase-educacion-listado.html", {"lista": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_motivoaumentosueldo", raise_exception=True)
def motivos_aumento_sueldo(request):
    return render(request, "motivos-aumento-sueldo.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_motivoaumentosueldo", raise_exception=True)
def motivos_aumento_sueldo_listado(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_motivosdespido"):
        listado = MotivoAumentoSueldo.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_motivosdespido"):
            listado = MotivoAumentoSueldo.objects.filter(
                active=True, empresa_reg=suc.empresa
            )
    return render(request, "motivos-aumento-sueldo-listado.html", {"lista": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_motivoaumentosueldo", raise_exception=True)
def motivo_aumento_sueldo_editar(request, id):
    dato = MotivoAumentoSueldo.objects.get(pk=id)
    return render(
        request, "motivos-aumento-sueldo.html", {"editar": True, "dato": dato}
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_educacion", raise_exception=True)
def educacion(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    clases_educacion = ClaseEducacion.objects.filter(
        active=True, empresa_reg=suc.empresa
    )
    return render(
        request,
        "educacion.html",
        {"empleados": empleados, "clasesEducacion": clases_educacion},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_educacion", raise_exception=True)
def educacion_editar(request, id):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    clases_educacion = ClaseEducacion.objects.filter(
        active=True, empresa_reg=suc.empresa
    )
    dato = Educacion.objects.get(pk=id)
    return render(
        request,
        "educacion.html",
        {
            "editar": True,
            "dato": dato,
            "empleados": empleados,
            "clasesEducacion": clases_educacion,
        },
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_educacion", raise_exception=True)
def educacion_listar(request):
    datos = []
    busqueda = None
    listado = None

    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(empresa_reg=suc.empresa)
    if "empleado" in request.GET:
        emp = request.GET.get("empleado")
        if len(emp) > 0:
            if int(emp) > 0:
                busqueda = int(emp)
                if request.user.has_perm("worksheet.see_all_motivosdespido"):
                    listado = Educacion.objects.filter(
                        empresa_reg=suc.empresa, empleado__pk=emp
                    )
                else:
                    if request.user.has_perm("worksheet.see_motivosdespido"):
                        listado = Educacion.objects.filter(
                            empleado__pk=emp, active=True, empresa_reg=suc.empresa
                        )

    return render(
        request,
        "educacion-listado.html",
        {"datos": listado, "empleados": empleados, "busqueda": busqueda},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_evaluacion", raise_exception=True)
def evaluacion(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "evaluacion.html", {"empleados": empleados})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_evaluacion", raise_exception=True)
def evaluacion_listar(request):
    datos = []
    busqueda = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.all()
    if "empleado" in request.GET:
        emp = request.GET.get("empleado")
        if len(emp) > 0:
            if int(emp) > 0:
                busqueda = int(emp)
                if request.user.has_perm("worksheet.see_all_evaluacion"):
                    datos = Evaluacion.objects.filter(
                        empleado__pk=emp, empresa_reg=suc.empresa
                    )
                else:
                    if request.user.has_perm("worksheet.see_evaluacion"):
                        datos = Evaluacion.objects.filter(
                            empleado__pk=emp, empresa_reg=suc.empresa, active=True
                        )
    return render(
        request,
        "evaluaciones-listado.html",
        {"datos": datos, "empleados": empleados, "busqueda": busqueda},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_evaluacion", raise_exception=True)
def evaluacion_editar(request, id):
    empleados = Employee.objects.filter(active=True)
    dato = Evaluacion.objects.get(pk=id)
    return render(
        request,
        "evaluacion.html",
        {"editar": True, "dato": dato, "empleados": empleados},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_empleosanteriores", raise_exception=True)
def empleo_anterior_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "empleos-anteriores.html", {"empleados": empleados})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_empleosanteriores", raise_exception=True)
def empleo_anterior_editar(request, id):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    dato = EmpleosAnteriores.objects.get(pk=id)
    return render(
        request,
        "empleos-anteriores.html",
        {"editar": True, "dato": dato, "empleados": empleados},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_empleosanteriores", raise_exception=True)
def empleo_anterior_listar(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    datos = []
    busqueda = None
    empleados = Employee.objects.filter(empresa_reg=suc.empresa)
    if "empleado" in request.GET:
        emp = request.GET.get("empleado")
        if len(emp) > 0:
            if int(emp) > 0:
                busqueda = int(emp)
                if request.user.has_perm("worksheet.see_all_evaluacion"):
                    datos = EmpleosAnteriores.objects.filter(
                        empleado__pk=emp, empresa_reg=suc.empresa
                    )
                else:
                    if request.user.has_perm("worksheet.see_evaluacion"):
                        datos = EmpleosAnteriores.objects.filter(
                            empleado__pk=emp, empresa_reg=suc.empresa, active=True
                        )
    return render(
        request,
        "empleos-anteriores-listado.html",
        {"datos": datos, "empleados": empleados, "busqueda": busqueda},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_grupocomisiones", raise_exception=True)
def grupo_comision(request):
    return render(request, "grupo-comisiones.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_grupocomisiones", raise_exception=True)
def grupo_comision_ditar(request, id):
    dato = GrupoComisiones.objects.get(pk=id)
    return render(request, "grupo-comisiones.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_grupocomisiones", raise_exception=True)
def grupo_comisiones_listar(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_grupocomisiones"):
        listado = GrupoComisiones.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_grupocomisiones"):
            listado = GrupoComisiones.objects.filter(
                active=True, empresa_reg=suc.empresa
            )
    return render(request, "grupo-comisiones-listado.html", {"datos": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_vendedor", raise_exception=True)
def vendedor_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    grp_com = GrupoComisiones.objects.filter(empresa_reg=suc.empresa)
    # empl_list = Vendedor.objects.filter(empresa_reg=suc.empresa).values_list('empleado__id', flat=True)
    # empleados = Employee.objects.exclude(pk__in=empl_list)
    # empleados = Employee.objects.filter(active=True)
    return render(request, "vendedor.html", {"grp_com": grp_com, "editar": False})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_vendedor", raise_exception=True)
def vendedor_editar(request, id):
    empleados = Employee.objects.filter(active=True)
    grp_com = GrupoComisiones.objects.all()
    dato = Vendedor.objects.get(pk=id)
    return render(
        request,
        "vendedor.html",
        {"editar": True, "dato": dato, "empleados": empleados, "grp_com": grp_com},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_vendedor", raise_exception=True)
def vendedor_listar(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_vendedor"):
        listado = Vendedor.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_vendedor"):
            listado = Vendedor.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "vendedor-listado.html", {"datos": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_feriado", raise_exception=True)
def feriado_form(request):
    return render(request, "feriado.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_feriado", raise_exception=True)
def feriado_editar(request, id):
    dato = Feriado.objects.get(pk=id)
    return render(request, "feriado.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_feriado", raise_exception=True)
def feriado_listar(request):
    listado = []
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_feriado"):
        listado = Feriado.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_feriado"):
            listado = Feriado.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "feriado-listado.html", {"datos": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_activoasignado", raise_exception=True)
def articulo_asignado_form(request):
    return render(request, "activo-asignado.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_activoasignado", raise_exception=True)
def articulo_asignado_editar(request, id):
    dato = ActivoAsignado.objects.get(pk=id)
    return render(request, "activo-asignado.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_activoasignado", raise_exception=True)
def articulos_asignados_listar(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_activoasignado"):
        listado = ActivoAsignado.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_activoasignado"):
            listado = ActivoAsignado.objects.filter(
                active=True, empresa_reg=suc.empresa
            )
    return render(request, "activos-asignados-listado.html", {"datos": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_termreason", raise_exception=True)
def motivo_rescision_contrato_form(request):
    return render(request, "motivos-rescision-contrato-form.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_termreason", raise_exception=True)
def motivo_rescision_contrato_editar(request, id):
    dato = TermReason.objects.get(pk=id)
    return render(
        request, "motivos-rescision-contrato-form.html", {"editar": True, "dato": dato}
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_termreason", raise_exception=True)
def motivo_rescicion_contrato_listar(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_termreason"):
        listado = TermReason.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_termreason"):
            listado = TermReason.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "motivo-rescision-contrato-listado.html", {"lista": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_salaryunit", raise_exception=True)
def tipo_salario_form(request):
    return render(request, "tipo-salario-form.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_salaryunit", raise_exception=True)
def tipo_salario_editar(request, id):
    dato = SalaryUnit.objects.get(pk=id)
    return render(request, "tipo-salario-form.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_salaryunit", raise_exception=True)
def tipo_salario_listar(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_salaryunit"):
        listado = SalaryUnit.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_salaryunit"):
            listado = SalaryUnit.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "tipo-salario-listado.html", {"lista": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_costunit", raise_exception=True)
def tipo_costo_empleado_form(request):
    return render(request, "costo-empleado-form.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_costunit", raise_exception=True)
def tipo_costo_empleado_editar(request, id):
    dato = CostUnit.objects.get(pk=id)
    return render(request, "costo-empleado-form.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_costunit", raise_exception=True)
def tipo_costo_empleado_listar(request):
    listado = []
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_costunit"):
        listado = CostUnit.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_costunit"):
            listado = CostUnit.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "costo-empleado-listado.html", {"lista": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_bank", raise_exception=True)
def banco_form(request):
    return render(request, "banco-formulario.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_bank", raise_exception=True)
def banco_editar(request, id):
    dato = Bank.objects.get(pk=id)
    return render(request, "banco-formulario.html", {"editar": True, "dato": dato})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_bank", raise_exception=True)
def banco_listado(request):
    listado = []
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_bank"):
        listado = Bank.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_bank"):
            listado = Bank.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "banco-listado.html", {"lista": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_usuarioempresa", raise_exception=True)
def usuario_empresa_form(request):
    frm = UsuarioEmpresaForm()
    suc = Branch.objects.get(pk=request.session["sucursal"])
    users = UsuarioEmpresa.objects.filter(empresa__grupo=suc.empresa.grupo)
    empresas = Empresa.objects.filter(grupo=suc.empresa.grupo)
    return render(
        request,
        "usuario-empresa.html",
        {"frm": frm, "users": users, "empresas": empresas},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_usuarioempresa", raise_exception=True)
def usuario_empresa_listar(request):
    listado = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_termreason"):
        listado = UsuarioEmpresa.objects.filter(usuario=request.user)
    else:
        if request.user.has_perm("worksheet.see_termreason"):
            listado = UsuarioEmpresa.objects.filter(active=True, usuario=request.user)
    return render(request, "usuario-empresa-listado.html", {"lista": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_usuarioempresa", raise_exception=True)
def usuario_empresa_editar(request, id):
    dato = UsuarioEmpresa.objects.get(pk=id)
    users = User.objects.all()
    empresas = Empresa.objects.all()
    return render(
        request,
        "usuario-empresa.html",
        {"editar": True, "dato": dato, "users": users, "empresas": empresas},
    )


# ---------------------------->>>> VISTAS AJAX <<<<----------------------------#
def guardar_empleado(request):
    mensaje = ""
    vSegundoNombre = None
    oPosicion = None
    oDepartamento = None
    oSucursal = None
    oEmpVentas = None
    oEstado = None
    oPais = None
    oEstadoTrabajo = None
    oPaisTrabajo = None
    oEstadoEmpleado = None
    oTerminoRescision = None
    oSex = None
    oJefe = None
    oBirthCountry = None
    oCivilStatus = None
    oCitizenShip = None
    oSalaryUnits = None
    oEmpCostUnit = None
    oBankCode = None
    try:
        if request.is_ajax():
            if request.method == "POST":
                pNom = request.POST["pNom"]
                sNom = request.POST["sNom"]
                apellido = request.POST["apellido"]
                puesto = ""
                no_ext = request.POST["numExt"]
                activo = request.POST["activo"]
                pos = request.POST["pos"]
                telOf = request.POST["telOf"]
                dept = request.POST["dept"]
                telExt = request.POST["telExt"]
                suc = request.POST["suc"]
                jefe = request.POST["jefe"]
                telMov = request.POST["telMov"]
                redsocial1 = request.POST["redsocial1"]
                slsP = request.POST["slsP"]
                redsocial2 = request.POST["redsocial2"]
                email = request.POST["email"]
                telCasa = request.POST["telCasa"]
                calle = request.POST["calle"]
                ncalle = request.POST["nCalle"]
                bloque = request.POST["bloque"]
                edif = request.POST["edif"]
                codPos = request.POST["codPos"]
                ciudad = request.POST["ciudad"]
                condado = request.POST["condado"]
                hdept = request.POST["hdept"]
                hpais = request.POST["hpais"]
                latitud = request.POST["latitud"]
                longitud = request.POST["longitud"]
                wcalle = request.POST["wcalle"]
                wncalle = request.POST["wncalle"]
                wbloque = request.POST["wbloque"]
                wedif = request.POST["wedif"]
                wcodPos = request.POST["wcodPost"]
                wciudad = request.POST["wciudad"]
                wcondado = request.POST["wcondado"]
                wdept = request.POST["wdept"]
                wpais = request.POST["wpais"]
                fechaCont = request.POST["fechaCont"]
                estEmp = request.POST["estEmp"]
                fechaRes = request.POST["fechaRES"]
                term = request.POST["term"]
                sexo = request.POST["sexo"]
                fecNac = request.POST["fecNac"]
                lugNac = request.POST["lugNac"]
                estCivil = request.POST["estCivil"]
                cantHijos = request.POST["cantHijos"]
                govID = request.POST["numID"]
                citiz = request.POST["citiz"]
                numPass = request.POST["numPass"]
                fecPassExt = request.POST["fecPassExt"]
                fecEmis = request.POST["fecEmis"]
                emisor = request.POST["emisor"]
                rtn = request.POST["rtn"]
                salary = request.POST["salario"]
                salario_diario = request.POST["salario_diario"]
                salaryUnits = request.POST["salarioUnd"]
                empCost = request.POST["costEmp"]
                empCostUnit = request.POST["costEmpUni"]
                banco = request.POST["banco"]
                numCuenta = request.POST["numCuenta"]
                branchBank = request.POST["bankSucursal"]
                remark = request.POST["comentarios"]
                metodo_pago = request.POST["metodo_pago"]

                if len(pNom) == 0:
                    mensaje = "El campo 'Primer Nombre' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(sNom) > 0:
                    vSegundoNombre = sNom

                if len(apellido) == 0:
                    mensaje = "El campo 'Apellido' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                # if len(puesto) == 0:
                #     mensaje = "El campo 'Denominación de Función' es obligatorio."
                #     data = {
                #         'mensaje': mensaje, 'error': True
                #     }
                #     return JsonResponse(data)

                if len(no_ext) == 0:
                    no_ext = None

                if len(pos) > 0:
                    if int(pos) > 0:
                        oPosicion = Position.objects.get(pk=pos)
                        if not oPosicion:
                            mensaje = "El 'Puesto de trabajo' no existe."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(dept) > 0:

                    if int(dept) > 0:
                        oDepartamento = Department.objects.get(pk=dept)
                        if not oDepartamento:
                            mensaje = "El 'Departamento' no existe."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(suc) > 0:
                    if int(suc) > 0:
                        oSucursal = Branch.objects.get(pk=suc)
                        if not oSucursal:
                            mensaje = "El 'Sucursal' no existe."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(jefe) > 0:
                    if int(jefe) > 0:
                        oJefe = Employee.objects.get(pk=jefe)
                        if not oJefe:
                            mensaje = "El 'Gerente' no existe."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(slsP) > 0:
                    if int(slsP) > 0:
                        oEmpVentas = Vendedor.objects.get(pk=slsP)
                        if not oSucursal:
                            mensaje = "El 'empleado de ventas' no existe."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(telOf) == 0:
                    telOf = None

                if len(telExt) == 0:
                    telExt = None

                if len(telMov) == 0:
                    telMov = None

                if len(telCasa) == 0:
                    telCasa == None

                if len(email) == 0:
                    email = None

                if len(calle) == 0:
                    calle = None

                if len(ncalle) == 0:
                    ncalle = None

                if len(edif) == 0:
                    edif = None

                if len(bloque) == 0:
                    bloque = None

                if len(codPos) == 0:
                    codPos = None

                if len(ciudad) == 0:
                    ciudad = None

                if len(condado) == 0:
                    condado = None

                if len(latitud) == 0:
                    latitud = None

                if len(longitud) == 0:
                    longitud = None

                if len(hdept) > 0:
                    if int(hdept) > 0:
                        oEstado = State.objects.get(pk=hdept)
                        if not oEstado:
                            mensaje = "El 'Estado/Departamento' no existe."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(hpais) > 0:
                    if int(hpais) > 0:
                        oPais = Country.objects.get(pk=hpais)
                        if not oPais:
                            mensaje = "El pais no existe en la base de datos."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(wcalle) == 0:
                    wcalle = None

                if len(wncalle) == 0:
                    wncalle = None

                if len(wbloque) == 0:
                    wbloque = None

                if len(wedif) == 0:
                    wedif = None

                if len(wcodPos) == 0:
                    wcodPos = None

                if len(wciudad) == 0:
                    wciudad = None

                if len(wcondado) == 0:
                    wcondado = None

                if len(redsocial1) == 0:
                    redsocial1 = None

                if len(redsocial2) == 0:
                    redsocial2 = None

                if len(wdept) > 0:
                    if int(wdept) > 0:
                        oEstadoTrabajo = State.objects.get(pk=wdept)
                        if not oEstadoTrabajo:
                            mensaje = (
                                "El estado de trabajo no existe en la base de datos."
                            )
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(wpais) > 0:
                    if int(wpais) > 0:
                        oPaisTrabajo = Country.objects.get(pk=wpais)
                        if not oPaisTrabajo:
                            mensaje = (
                                "El país de trabajo no existe en la base de datos."
                            )
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(fechaCont) == 0:
                    fechaCont = None

                if len(estEmp) > 0:
                    if int(estEmp) > 0:
                        oEstadoEmpleado = StatusEmp.objects.get(pk=estEmp)
                        if not oEstadoEmpleado:
                            mensaje = (
                                "El estado de empleado no existe en la base de datos."
                            )
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(fechaRes) == 0:
                    fechaRes = None

                if len(term) > 0:
                    if int(term) > 0:
                        oTerminoRescision = TermReason.objects.get(pk=term)
                        if not oTerminoRescision:
                            mensaje = (
                                "El término de rescisión no existe en la base de datos."
                            )
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(sexo) > 0:
                    if int(sexo) > 0:
                        oSex = Sex.objects.get(pk=sexo)
                        if not oSex:
                            mensaje = "El sexo no existe en la base de datos."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(fecNac) == 0:
                    fecNac = None

                if len(lugNac) > 0:
                    if int(lugNac) > 0:
                        oBirthCountry = Country.objects.get(pk=lugNac)
                        if not oBirthCountry:
                            mensaje = (
                                "El lugar de nacimiento no existe en la base de datos."
                            )
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(estCivil) > 0:
                    if int(estCivil) > 0:
                        oCivilStatus = CivilStatus.objects.get(pk=estCivil)
                        if not oCivilStatus:
                            mensaje = "El estado civil no existe en la base de datos."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(citiz) > 0:
                    if int(citiz) > 0:
                        oCitizenShip = Country.objects.get(pk=citiz)
                        if not oCitizenShip:
                            mensaje = "La nacionalidad no existe en la base de datos."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                if len(fecPassExt) == 0:
                    fecPassExt = None

                if len(fecEmis) == 0:
                    fecEmis = None

                if len(rtn) == 0:
                    rtn = None

                if len(salaryUnits) > 0:
                    if int(salaryUnits) > 0:
                        oSalaryUnits = SalaryUnit.objects.get(pk=salaryUnits)
                        if not oSalaryUnits:
                            mensaje = (
                                "El tipo de salario no existe en la base de datos."
                            )
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(empCostUnit) > 0:
                    if int(empCostUnit) > 0:
                        oEmpCostUnit = CostUnit.objects.get(pk=empCostUnit)
                        if not oEmpCostUnit:
                            mensaje = "El tipo de costo de empleado no existe en la base de datos."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(banco) > 0:
                    if int(banco) > 0:
                        oBankCode = Bank.objects.get(pk=banco)

                        if not oBankCode:
                            mensaje = "El banco no existe en la base de datos."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(empCost) == 0:
                    empCost = None

                if len(salary) == 0:
                    salary = None

                if len(salario_diario) == 0:
                    salario_diario = None

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oEmpleado = Employee(
                    firstName=pNom,
                    middleName=vSegundoNombre,
                    lastName=apellido,
                    extEmpNo=no_ext,
                    jobTitle=puesto,
                    user_reg=request.user,
                    active=activo,
                    position=oPosicion,
                    officeTel=telOf,
                    dept=oDepartamento,
                    officeExt=telExt,
                    branch=oSucursal,
                    jefe=oJefe,
                    mobile=telMov,
                    socialNetwork1=redsocial1,
                    socialNetwork2=redsocial2,
                    slsPerson=oEmpVentas,
                    email=email,
                    homeTel=telCasa,
                    homeStreet=calle,
                    streetNoH=ncalle,
                    homeBlock=bloque,
                    homeBuild=edif,
                    homeZip=codPos,
                    homeCity=ciudad,
                    homeCounty=condado,
                    homeState=oEstado,
                    homeCountry=oPais,
                    lat=latitud,
                    lng=longitud,
                    workStreet=wcalle,
                    streetNoW=wncalle,
                    workBlock=wbloque,
                    workBuild=wedif,
                    workZip=wcodPos,
                    workCity=wciudad,
                    workCounty=wcondado,
                    workState=oEstadoTrabajo,
                    workCountry=oPaisTrabajo,
                    startDate=fechaCont,
                    status=oEstadoEmpleado,
                    termDate=fechaRes,
                    termReason=oTerminoRescision,
                    sex=oSex,
                    birthDate=fecNac,
                    birthCountry=oBirthCountry,
                    marrStatus=oCivilStatus,
                    nChildren=cantHijos,
                    govID=govID,
                    citizenship=oCitizenShip,
                    passportNo=numPass,
                    passportExt=fecPassExt,
                    passIssue=fecEmis,
                    passIssuer=emisor,
                    rtn=rtn,
                    salary=salary,
                    salario_diario=salario_diario,
                    salaryUnits=oSalaryUnits,
                    empCost=empCost,
                    empCostUnit=oEmpCostUnit,
                    bankCode=oBankCode,
                    bankAccount=numCuenta,
                    branchBank=branchBank,
                    remark=remark,
                    metodo_pago=metodo_pago,
                    empresa_reg=suc.empresa,
                )
                oEmpleado.save()

                mensaje = "Se ha guardado el registro del empleado"
                data = {"mensaje": mensaje, "error": False}
                return JsonResponse(data)
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": "Error: ",
        }
        return JsonResponse(data)


def actualizar_empleado(request):
    mensaje = ""
    oPosicion = None
    oDepartamento = None
    oSucursal = None
    oEmpVentas = None
    oEstado = None
    oPais = None
    oEstadoTrabajo = None
    oPaisTrabajo = None
    oEstadoEmpleado = None
    oTerminoRescision = None
    oJefe = None
    oSex = None
    oBirthCountry = None
    oCivilStatus = None
    oCitizenShip = None
    oSalaryUnits = None
    oEmpCostUnit = None
    oTipoNomina = None
    oTipoContrato = None
    oBankCode = None
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = request.POST["id"]
                pNom = request.POST["pNom"]
                sNom = request.POST["sNom"]
                apellido = request.POST["apellido"]
                # puesto = request.POST['puesto']
                no_ext = request.POST["numExt"]
                activo = request.POST["activo"]
                pos = request.POST["pos"]
                telOf = request.POST["telOf"]
                dept = request.POST["dept"]
                telExt = request.POST["telExt"]
                suc = request.POST["suc"]
                jefe = request.POST["jefe"]
                telMov = request.POST["telMov"]
                redsocial1 = request.POST["redsocial1"]
                slsP = request.POST["slsP"]
                redsocial2 = request.POST["redsocial2"]
                email = request.POST["email"]
                telCasa = request.POST["telCasa"]
                calle = request.POST["calle"]
                ncalle = request.POST["nCalle"]
                bloque = request.POST["bloque"]
                edif = request.POST["edif"]
                codPos = request.POST["codPos"]
                ciudad = request.POST["ciudad"]
                condado = request.POST["condado"]
                hdept = request.POST["hdept"]
                hpais = request.POST["hpais"]
                latitud = request.POST["latitud"]
                longitud = request.POST["longitud"]
                wcalle = request.POST["wcalle"]
                wncalle = request.POST["wncalle"]
                wbloque = request.POST["wbloque"]
                wedif = request.POST["wedif"]
                wcodPos = request.POST["wcodPost"]
                wciudad = request.POST["wciudad"]
                wcondado = request.POST["wcondado"]
                wdept = request.POST["wdept"]
                wpais = request.POST["wpais"]
                fechaCont = request.POST["fechaCont"]
                estEmp = request.POST["estEmp"]
                fechaRes = request.POST["fechaRES"]
                term = request.POST["term"]
                sexo = request.POST["sexo"]
                fecNac = request.POST["fecNac"]
                lugNac = request.POST["lugNac"]
                estCivil = request.POST["estCivil"]
                cantHijos = request.POST["cantHijos"]
                govID = request.POST["numID"]
                citiz = request.POST["citiz"]
                numPass = request.POST["numPass"]
                fecPassExt = request.POST["fecPassExt"]
                fecEmis = request.POST["fecEmis"]
                emisor = request.POST["emisor"]
                rtn = request.POST["rtn"]
                salary = request.POST["salario"]
                salario_diario = request.POST["salario_diario"]
                salaryUnits = request.POST["salarioUnd"]
                empCost = request.POST["costEmp"]
                empCostUnit = request.POST["costEmpUni"]
                banco = request.POST["banco"]
                numCuenta = request.POST["numCuenta"]
                branchBank = request.POST["bankSucursal"]
                remark = request.POST["comentarios"]
                metodo_pago = request.POST["metodo_pago"]
                tipo_nomina = request.POST["tipo_nomina"]
                tipo_contrato = request.POST["tipo_contrato"]

                if len(pNom) == 0:
                    mensaje = "El campo 'Primer Nombre' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(sNom) == 0:
                    sNom = None

                if len(apellido) == 0:
                    mensaje = "El campo 'Apellido' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                # if len(puesto) == 0:
                #     mensaje = "El campo 'Puesto de trabajo' es obligatorio."
                #     data = {
                #         'mensaje': mensaje, 'error': True
                #     }
                #     return JsonResponse(data)

                if len(no_ext) == 0:
                    no_ext = None

                if len(pos) > 0:
                    if int(pos) > 0:
                        oPosicion = Position.objects.get(pk=pos)
                        if not oPosicion:
                            mensaje = "El 'Puesto de trabajo' no existe."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(dept) > 0:
                    if int(dept) > 0:
                        oDepartamento = Department.objects.get(pk=dept)
                        if not oDepartamento:
                            mensaje = "El 'Departamento' no existe."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(suc) > 0:
                    if int(suc) > 0:
                        oSucursal = Branch.objects.get(pk=suc)
                        if not oSucursal:
                            mensaje = "El 'Sucursal' no existe."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(jefe) > 0:
                    if int(jefe) > 0:
                        oJefe = Employee.objects.get(pk=jefe)
                        if not oJefe:
                            mensaje = "El 'Gerente' no existe."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(slsP) > 0:
                    if int(slsP) > 0:
                        oEmpVentas = SalesPerson.objects.get(pk=slsP)
                        if not oSucursal:
                            mensaje = "El 'empleado de ventas' no existe."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(telOf) == 0:
                    telOf = None

                if len(telExt) == 0:
                    telExt = None

                if len(telMov) == 0:
                    telMov = None

                if len(telCasa) == 0:
                    telCasa = None

                if len(email) == 0:
                    email = None

                if len(calle) == 0:
                    calle = None

                if len(ncalle) == 0:
                    ncalle = None

                if len(edif) == 0:
                    edif = None

                if len(bloque) == 0:
                    bloque = None

                if len(codPos) == 0:
                    codPos = None

                if len(ciudad) == 0:
                    ciudad = None

                if len(condado) == 0:
                    condado = None

                if len(redsocial1) == 0:
                    redsocial = None

                if len(redsocial2) == 0:
                    redsocial2 = None

                if len(latitud) == 0:
                    latitud = None

                if len(longitud) == 0:
                    longitud = None

                if len(hdept) > 0:
                    if int(hdept) > 0:
                        oEstado = State.objects.get(pk=hdept)
                        if not oEstado:
                            mensaje = "El 'Estado/Departamento' no existe."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(hpais) > 0:
                    if int(hpais) > 0:
                        oPais = Country.objects.get(pk=hpais)
                        if not oPais:
                            mensaje = "El pais no existe en la base de datos."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(wcalle) == 0:
                    wcalle = None

                if len(wncalle) == 0:
                    wncalle = None

                if len(wbloque) == 0:
                    wbloque = None

                if len(wedif) == 0:
                    wedif = None

                if len(wcodPos) == 0:
                    wcodPos = None

                if len(wciudad) == 0:
                    wciudad = None

                if len(wcondado) == 0:
                    wcondado = None

                if len(rtn) == 0:
                    rtn = None

                if len(wdept) > 0:
                    if int(wdept) > 0:
                        oEstadoTrabajo = State.objects.get(pk=wdept)
                        if not oEstadoTrabajo:
                            mensaje = (
                                "El estado de trabajo no existe en la base de datos."
                            )
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(wpais) > 0:
                    if int(wpais) > 0:
                        oPaisTrabajo = Country.objects.get(pk=wpais)
                        if not oPaisTrabajo:
                            mensaje = (
                                "El país de trabajo no existe en la base de datos."
                            )
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(fechaCont) == 0:
                    fechaCont = None

                if len(estEmp) > 0:
                    if int(estEmp) > 0:
                        oEstadoEmpleado = StatusEmp.objects.get(pk=estEmp)
                        if not oEstadoEmpleado:
                            mensaje = (
                                "El estado de empleado no existe en la base de datos."
                            )
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(fechaRes) == 0:
                    fechaRes = None

                if len(term) > 0:
                    if int(term) > 0:
                        oTerminoRescision = TermReason.objects.get(pk=term)
                        if not oTerminoRescision:
                            mensaje = (
                                "El término de rescisión no existe en la base de datos."
                            )
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(sexo) > 0:
                    if int(sexo) > 0:
                        oSex = Sex.objects.get(pk=sexo)
                        if not oSex:
                            mensaje = "El sexo no existe en la base de datos."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(fecNac) == 0:
                    fecNac = None

                if len(lugNac) > 0:
                    if int(lugNac) > 0:
                        oBirthCountry = Country.objects.get(pk=lugNac)
                        if not oBirthCountry:
                            mensaje = (
                                "El lugar de nacimiento no existe en la base de datos."
                            )
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(estCivil) > 0:
                    if int(estCivil) > 0:
                        oCivilStatus = CivilStatus.objects.get(pk=estCivil)
                        if not oCivilStatus:
                            mensaje = "El estado civil no existe en la base de datos."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(citiz) > 0:
                    if int(citiz) > 0:
                        oCitizenShip = Country.objects.get(pk=citiz)
                        if not oCitizenShip:
                            mensaje = "La nacionalidad no existe en la base de datos."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                if len(fecPassExt) == 0:
                    fecPassExt = None

                if len(fecEmis) == 0:
                    fecEmis = None

                if len(salaryUnits) > 0:
                    if int(salaryUnits) > 0:
                        oSalaryUnits = SalaryUnit.objects.get(pk=salaryUnits)
                        if not oSalaryUnits:
                            mensaje = (
                                "El tipo de salario no existe en la base de datos."
                            )
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(tipo_contrato) > 0:
                    if int(tipo_contrato) > 0:
                        oTipoContrato = TipoContrato.objects.get(pk=tipo_contrato)
                        if not oTipoContrato:
                            mensaje = (
                                "El tipo de contrato no existe en la base de datos."
                            )
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(tipo_nomina) > 0:
                    if int(tipo_nomina) > 0:
                        oTipoNomina = TipoNomina.objects.get(pk=tipo_nomina)
                        if not oTipoNomina:
                            mensaje = "El tipo de nomina no existe en la base de datos."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(empCostUnit) > 0:
                    if int(empCostUnit) > 0:
                        oEmpCostUnit = CostUnit.objects.get(pk=empCostUnit)
                        if not oEmpCostUnit:
                            mensaje = "El tipo de costo de empleado no existe en la base de datos."
                            data = {"mensaje": mensaje, "error": True}
                            return JsonResponse(data)

                if len(empCost) == 0:
                    empCost = None

                if len(salary) == 0:
                    salary = None

                if len(salario_diario) == 0:
                    salario_diario = None

                if len(metodo_pago) == 0:
                    mensaje = "Seleccione un método de pago."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if metodo_pago == "2":
                    if len(banco) > 0:
                        if int(banco) > 0:
                            oBankCode = Bank.objects.get(pk=banco)

                            if not oBankCode:
                                mensaje = "El banco no existe en la base de datos."
                                data = {"mensaje": mensaje, "error": True}
                                return JsonResponse(data)

                    if len(numCuenta) == 0:
                        mensaje = "El campo 'Numero de Cuenta' es obligatorio."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                oEmp = Employee.objects.get(pk=id)
                oEmp.firstName = pNom
                oEmp.middleName = sNom
                oEmp.lastName = apellido
                oEmp.extEmpNo = no_ext
                oEmp.jobTitle = ""
                oEmp.position = oPosicion
                oEmp.dept = oDepartamento
                oEmp.branch = oSucursal
                oEmp.jefe = oJefe
                oEmp.slsPerson = oEmpVentas
                oEmp.officeTel = telOf
                oEmp.officeExt = telExt
                oEmp.mobile = telMov
                oEmp.socialNetwork1 = redsocial1
                oEmp.homeTel = telCasa
                oEmp.socialNetwork2 = redsocial2
                oEmp.email = email
                oEmp.homeStreet = calle
                oEmp.streetNoH = ncalle
                oEmp.homeBuild = edif
                oEmp.homeBlock = bloque
                oEmp.homeZip = codPos
                oEmp.homeCity = ciudad
                oEmp.homeCounty = condado
                oEmp.homeState = oEstado
                oEmp.homeCountry = oPais
                oEmp.lat = latitud
                oEmp.lng = longitud
                oEmp.workStreet = wcalle
                oEmp.streetNoW = wncalle
                oEmp.workBlock = wbloque
                oEmp.workBuild = wedif
                oEmp.workZip = wcodPos
                oEmp.workCity = wciudad
                oEmp.workCounty = wcondado
                oEmp.workState = oEstadoTrabajo
                oEmp.workCountry = oPaisTrabajo
                oEmp.startDate = fechaCont
                oEmp.status = oEstadoEmpleado
                oEmp.termDate = fechaRes
                oEmp.termReason = oTerminoRescision
                oEmp.sex = oSex
                oEmp.birthDate = fecNac
                oEmp.birthCountry = oBirthCountry
                oEmp.marrStatus = oCivilStatus
                oEmp.nChildren = cantHijos
                oEmp.govID = govID
                oEmp.citizenship = oCitizenShip
                oEmp.passportNo = numPass
                oEmp.passportExt = fecPassExt
                oEmp.passIssue = fecEmis
                oEmp.passIssuer = emisor
                oEmp.rtn = rtn
                oEmp.salary = salary
                oEmp.salario_diario = salario_diario
                oEmp.salaryUnits = oSalaryUnits
                oEmp.empCost = empCost
                oEmp.empCostUnit = oEmpCostUnit
                oEmp.bankCode = oBankCode
                oEmp.bankAccount = numCuenta
                oEmp.branchBank = branchBank
                oEmp.remark = remark
                oEmp.metodo_pago = metodo_pago
                oEmp.tipo_contrato = oTipoContrato
                oEmp.tipo_nomina = oTipoNomina

                oEmp.active = activo
                oEmp.user_mod = request.user
                oEmp.date_mod = datetime.datetime.now()
                oEmp.save()

                mensaje = "Se ha actualizado el registro del Empleado"
                data = {"mensaje": mensaje, "error": False, "editar": True}
            else:
                mensaje = "Metodo no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_empleado(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = Employee.objects.get(pk=reg_id)
                    oMd.delete()
                    mensaje = "Se ha eliminado el registro del empleado"
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    # return HttpResponseRedirect('/listar/corporativos/')
    return JsonResponse(data)


def obtener_antiguedad(request):
    data = {}
    if request.is_ajax():
        fecha = request.GET.get("fecha")
        fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d")
        rd = relativedelta.relativedelta(datetime.datetime.today(), date(fecha.year, fecha.month, fecha.day))
        antiguedad = "{0.years} años, {0.months} meses y {0.days} días".format(rd)
        data = {"antiguedad": antiguedad}
    return JsonResponse(data)


def guardar_corporativo(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                razon = request.POST["razon"]
                nombre = request.POST["organiz"]
                activo = int(request.POST["activo"])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                if len(razon) > 0:
                    oGrupo = GrupoCorporativo(
                        razonSocial=razon,
                        nombreComercial=nombre,
                        empresa_reg=suc.empresa,
                        active=activo,
                        user_reg=request.user,
                    )
                    oGrupo.save()
                    grupo = {
                        "pk": oGrupo.pk,
                        "razon": oGrupo.razonSocial,
                        "nombre": oGrupo.nombreComercial,
                        "activo": oGrupo.active,
                    }
                    mensaje = "Se ha guardado el registro del Grupo Corporativo"
                    data = {"grupo": grupo, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Metodo no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_corporativo(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = request.POST["id"]
                razon = request.POST["razon"]
                nombre = request.POST["organiz"]
                activo = int(request.POST["activo"])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(razon) > 0:
                    oGrupo = GrupoCorporativo.objects.get(pk=id)
                    # day  = timezone.now()
                    # formatedDay  = day.strftime("%Y-%m-%d %H:%M:%S")
                    oGrupo.razonSocial = razon
                    oGrupo.nombreComercial = nombre
                    oGrupo.active = activo
                    oGrupo.user_mod = request.user
                    oGrupo.date_mod = datetime.datetime.now()
                    # oGrupo = GrupoCorporativo(
                    #     razonSocial = razon,
                    #     nombreComercial = nombre,
                    #     active = activo,
                    #     user_reg=request.user,
                    # )
                    oGrupo.save()
                    grupo = {
                        "pk": oGrupo.pk,
                        "razon": oGrupo.razonSocial,
                        "nombre": oGrupo.nombreComercial,
                        "activo": oGrupo.active,
                    }
                    mensaje = "Se ha actualizado el registro del Grupo Corporativo"
                    data = {"grupo": grupo, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Metodo no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_corporativo(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oGrupo = GrupoCorporativo.objects.get(pk=reg_id)
                    oGrupo.delete()
                    mensaje = "Se ha eliminado el registro del Grupo Corporativo"
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    # return HttpResponseRedirect('/listar/corporativos/')
    return JsonResponse(data)


def guardar_empresa(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                razon = request.POST["razon"]
                nombre = request.POST["organiz"]
                activo = int(request.POST["activo"])

                if len(razon) == 0:
                    mensaje = "El campo 'Razón social' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(razon) > 100:
                    mensaje = (
                        "El campo 'Razón social' tiene como máximo 100 caracteres."
                    )
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre comercial' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(nombre) > 100:
                    mensaje = (
                        "El campo 'Nombre comercial' tiene como máximo 100 caracteres."
                    )
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                tot_reg = Empresa.objects.filter(razonSocial=razon).count()
                if tot_reg > 0:
                    mensaje = "Ya existe un registro con la razón social ingresada."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                tot_reg = Empresa.objects.filter(nombreComercial=nombre).count()
                if tot_reg > 0:
                    mensaje = "Ya existe un registro con el nombre comercial ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oEmpresa = Empresa(
                    razonSocial=razon,
                    nombreComercial=nombre,
                    grupo=suc.empresa.grupo,
                    active=activo,
                    user_reg=request.user,
                )
                oEmpresa.save()
                grupo = {
                    "pk": oEmpresa.pk,
                    "razon": oEmpresa.razonSocial,
                    "nombre": oEmpresa.nombreComercial,
                    "activo": oEmpresa.active,
                }
                mensaje = "Se ha guardado el registro de la empresa"
                data = {"grupo": grupo, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Metodo no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_empresa(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = request.POST["id"]
                nombre = request.POST["organiz"]
                activo = int(request.POST["activo"])

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre comercial' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(nombre) > 100:
                    mensaje = (
                        "El campo 'Nombre comercial' tiene como máximo 100 caracteres."
                    )
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oEmp = Empresa.objects.get(pk=id)
                if oEmp:
                    oEmp.nombreComercial = nombre
                    oEmp.active = activo
                    oEmp.user_mod = request.user
                    oEmp.date_mod = datetime.datetime.now()
                    oEmp.save()
                    emp = {
                        "pk": oEmp.pk,
                        "razon": oEmp.razonSocial,
                        "nombre": oEmp.nombreComercial,
                        "activo": oEmp.active,
                    }
                    mensaje = "Se ha actualizado el registro de la empresa"
                    data = {"emp": emp, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "El registro no existe."
                    data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Metodo no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def eliminar_empresa(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oEmp = Empresa.objects.get(pk=reg_id)
                    if oEmp:
                        oEmp.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_sucursal(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                nombre = request.POST["nombre"]
                descripcion = request.POST["descripcion"]
                activo = int(request.POST["activo"])

                if len(nombre) == 0:
                    mensaje = "El campo 'Código' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(nombre) > 5:
                    mensaje = "El campo 'Código' tiene como máximo 5 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(descripcion) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(descripcion) > 150:
                    mensaje = "El campo 'Descripción' tiene como máximo 150 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                tot_reg = Branch.objects.filter(
                    code=nombre, empresa=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existe un registro con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oSucursal = Branch(
                    code=nombre,
                    description=descripcion,
                    empresa=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oSucursal.save()
                grupo = {
                    "pk": oSucursal.pk,
                    "nombre": oSucursal.code,
                    "descripcion": oSucursal.description,
                    "activo": oSucursal.active,
                }
                mensaje = "Se ha guardado el registro de la sucursal"
                data = {"grupo": grupo, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Metodo no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def actualizar_sucursal(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = request.POST["id"]
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = "El campo 'Descripción' tiene como máximo 150 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oSucursal = Branch.objects.get(pk=id)

                if oSucursal:
                    oSucursal.description = desc
                    oSucursal.active = activo
                    oSucursal.user_mod = request.user
                    oSucursal.date_mod = datetime.datetime.now()
                    oSucursal.save()
                    sucursal = {
                        "pk": oSucursal.pk,
                        "desc": oSucursal.description,
                        "nombre": oSucursal.code,
                        "activo": oSucursal.active,
                    }
                    mensaje = "Se ha actualizado el registro de la Sucursal"
                    data = {"sucursal": sucursal, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Metodo no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def eliminar_sucursal(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oSucursal = Branch.objects.get(pk=reg_id)
                    oSucursal.delete()
                    mensaje = "Se ha eliminado el registro de la sucursal"
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def guardar_division(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                code = request.POST["code"]
                descripcion = request.POST["descripcion"]
                activo = int(request.POST["activo"])

                if len(code) == 0:
                    mensaje = "El campo 'Código' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = "El campo 'Código' tiene un maximo de 5 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(descripcion) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(descripcion) > 150:
                    mensaje = (
                        "El campo 'Descripción' tiene un maximo de 150 caracteres."
                    )
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                tot_reg = Divisiones.objects.filter(
                    code=code, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existe un registro con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oDivision = Divisiones(
                    code=code,
                    descripcion=descripcion,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oDivision.save()
                grupo = {
                    "pk": oDivision.pk,
                    "descripcion": oDivision.descripcion,
                    "activo": oDivision.active,
                }
                mensaje = "Se ha guardado el registro de la División"
                data = {"grupo": grupo, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Metodo no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_division(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = request.POST["id"]
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = (
                        "El campo 'Descripción' tiene un maximo de 150 caracteres."
                    )
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oDiv = Divisiones.objects.get(pk=id)

                if oDiv:
                    oDiv.descripcion = desc
                    oDiv.active = activo
                    oDiv.user_mod = request.user
                    oDiv.date_mod = datetime.datetime.now()
                    oDiv.save()
                    division = {
                        "pk": oDiv.pk,
                        "desc": oDiv.descripcion,
                        "activo": oDiv.active,
                    }
                    mensaje = "Se ha actualizado el registro."
                    data = {"division": division, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_division(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oDivision = Divisiones.objects.get(pk=reg_id)
                    if oDivision:
                        oDivision.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_departamento(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                nombre = request.POST["nombre"]
                descripcion = request.POST["descripcion"]
                activo = int(request.POST["activo"])

                if len(nombre) == 0:
                    mensaje = "El campo 'Código' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(nombre) > 5:
                    mensaje = (
                        "El campo 'Código' debe ser tener como máximo 5 caracteres."
                    )
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(descripcion) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(descripcion) > 150:
                    mensaje = "El campo 'Descripción' tiene como máximo 150 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                tot_reg = Department.objects.filter(
                    code=nombre, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existen registros con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oDeparment = Department(
                    code=nombre,
                    description=descripcion,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oDeparment.save()
                grupo = {
                    "pk": oDeparment.pk,
                    "codigo": oDeparment.code,
                    "descripcion": oDeparment.description,
                    "activo": oDeparment.active,
                }
                mensaje = "Se ha guardado el registro del Departamento"
                data = {"grupo": grupo, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Metodo no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_departamento(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = request.POST["id"]
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = "El campo 'Descripción' tiene como máximo 150 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oDep = Department.objects.get(pk=id)

                if oDep:
                    oDep.description = desc
                    oDep.active = activo
                    oDep.user_mod = request.user
                    oDep.date_mod = datetime.datetime.now()
                    oDep.save()
                    dep = {
                        "pk": oDep.pk,
                        "name": oDep.code,
                        "desc": oDep.description,
                        "activo": oDep.active,
                    }
                    mensaje = "Se ha actualizado el registro."
                    data = {"departamento": dep, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_departamento(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oDivision = Department.objects.get(pk=reg_id)
                    totReg = Employee.objects.filter(dept__pk=reg_id).count()
                    if oDivision:
                        if totReg == 0:
                            oDivision.delete()
                            mensaje = "Se ha eliminado el registro."
                            data = {"mensaje": mensaje, "error": False}
                        else:
                            mensaje = "Existen datos asociados al registro que quiere eliminar."
                            data = {"mensaje": mensaje, "error": True}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_puesto(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                nombre = request.POST["nombre"]
                descripcion = request.POST["descripcion"]
                funcion_operativa = request.POST["funcion_operativa"]
                activo = int(request.POST["activo"])

                if len(nombre) == 0:
                    data = {
                        "error": True,
                        "mensaje": 'El campo "Código" es obligatorio.',
                    }
                    return JsonResponse(data)

                if len(nombre) > 5:
                    data = {
                        "error": True,
                        "mensaje": 'El campo "Código" debe tener un máximo de 5 caracteres.',
                    }
                    return JsonResponse(data)

                if len(descripcion) == 0:
                    data = {
                        "error": True,
                        "mensaje": 'El campo "Descripción" es obligatorio.',
                    }
                    return JsonResponse(data)

                if len(descripcion) > 150:
                    data = {
                        "error": True,
                        "mensaje": 'El campo "Descripción" debe tener un máximo de 150 caracteres.',
                    }
                    return JsonResponse(data)

                if len(funcion_operativa) == 0:
                    data = {
                        "error": True,
                        "mensaje": 'Ingrese un valor válido para el campo "Función Operativa".',
                    }
                    return JsonResponse(data)

                if int(funcion_operativa) == 0:
                    data = {
                        "error": True,
                        "mensaje": 'Seleccione un valor para el campo "Función Operativa".',
                    }
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                oFun = FuncionesTrabajo.objects.get(pk=funcion_operativa)
                tot_reg = Position.objects.filter(
                    code=nombre, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    data = {
                        "error": True,
                        "mensaje": "Ya existen registros con el código ingresado.",
                    }
                    return JsonResponse(data)

                if len(nombre) > 0 and len(descripcion) > 0:
                    oPuesto = Position(
                        code=nombre,
                        description=descripcion,
                        empresa_reg=suc.empresa,
                        funcion_operativa=oFun,
                        active=activo,
                        user_reg=request.user,
                    )
                    oPuesto.save()
                    grupo = {
                        "pk": oPuesto.pk,
                        "descripcion": oPuesto.description,
                        "activo": oPuesto.active,
                    }
                    mensaje = "Se ha guardado el registro del Puesto de Trabajo"
                    data = {"grupo": grupo, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Metodo no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_puesto(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                funcion_operativa = request.POST["funcion_operativa"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    data = {
                        "error": True,
                        "mensaje": 'El campo "Descripción" es obligatorio.',
                    }
                    return JsonResponse(data)

                if len(desc) > 150:
                    data = {
                        "error": True,
                        "mensaje": 'El campo "Descripción" debe tener un máximo de 150 caracteres.',
                    }
                    return JsonResponse(data)

                if int(funcion_operativa) == 0:
                    data = {
                        "error": True,
                        "mensaje": 'Ingrese un valor válido para el campo "Función Operativa".',
                    }
                    return JsonResponse(data)

                if funcion_operativa == 0:
                    data = {
                        "error": True,
                        "mensaje": 'Seleccione un valor para el campo "Función Operativa".',
                    }
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oPos = Position.objects.get(pk=id)
                oFun = FuncionesTrabajo.objects.get(pk=funcion_operativa)

                if oPos:
                    oPos.description = desc
                    oPos.active = activo
                    oPos.user_mod = request.user
                    oPos.date_mod = datetime.datetime.now()
                    oPos.funcion_operativa = oFun
                    oPos.save()
                    pos = {
                        "pk": oPos.pk,
                        "name": oPos.code,
                        "desc": oPos.description,
                        "activo": oPos.active,
                    }
                    mensaje = "Se ha actualizado el registro."
                    data = {"puesto": pos, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_puesto(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oPuesto = Position.objects.get(pk=reg_id)
                    totReg = Employee.objects.filter(dept__pk=reg_id).count()
                    if oPuesto:
                        if totReg == 0:
                            oPuesto.delete()
                            mensaje = "Se ha eliminado el registro."
                            data = {"mensaje": mensaje, "error": False}
                        else:
                            mensaje = "Existen datos asociados al registro que quiere eliminar."
                            data = {"mensaje": mensaje, "error": True}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def obtenerPuestos(request):
    data = {}
    puestos = []
    if request.is_ajax():
        funcion_id = request.GET.get("funcion_id")
        tot_reg = FuncionesTrabajo.objects.filter(id=funcion_id).count()
        if tot_reg > 0:
            o_func = FuncionesTrabajo.objects.get(id=funcion_id)
            puestos = Position.objects.filter(funcion_operativa=o_func)
    return render(request, "ajax/puestos.html", {"positions": puestos})


def guardar_ccosto(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                code = request.POST["code"]
                descripcion = request.POST["descripcion"]
                activo = int(request.POST["activo"])

                if len(code) == 0:
                    mensaje = 'El campo "Código" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = 'El campo "Código" tiene como máximo 5 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(descripcion) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(descripcion) > 150:
                    mensaje = 'El campo "Descripción" tiene como máximo 150 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                tot_reg = CentrosCostos.objects.filter(
                    code=code, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existe un registro con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oCCosto = CentrosCostos(
                    code=code,
                    descripcion=descripcion,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oCCosto.save()
                grupo = {
                    "pk": oCCosto.pk,
                    "descripcion": oCCosto.descripcion,
                    "activo": oCCosto.active,
                }
                mensaje = "Se ha guardado el registro del Centro de Costos"
                data = {"grupo": grupo, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def actualizar_ccosto(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = 'El campo "Descripción" tiene como máximo 150 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oCC = CentrosCostos.objects.get(pk=id)

                if oCC:
                    oCC.descripcion = desc
                    oCC.active = activo
                    oCC.user_mod = request.user
                    oCC.date_mod = datetime.now()
                    oCC.save()
                    CC = {
                        "pk": oCC.pk,
                        "desc": oCC.descripcion,
                        "activo": oCC.active,
                    }
                    mensaje = "Se ha actualizado el registro."
                    data = {"puesto": CC, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def eliminar_ccosto(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oCC = CentrosCostos.objects.get(pk=reg_id)
                    if oCC:
                        oCC.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_pais(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                codigo = request.POST["codigo"]
                nombre = request.POST["nombre"]
                activo = int(request.POST["activo"])

                if len(codigo) == 0:
                    mensaje = "El campo 'Código' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(nombre) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(codigo) > 5:
                    mensaje = "El campo 'Código' tiene como máximo 5 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(nombre) > 150:
                    mensaje = "El campo 'Descripcion' tiene como máximo 150 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                tot_reg = Country.objects.filter(
                    code=codigo, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existen registros con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(nombre) > 0 and len(codigo) > 0:
                    oCountry = Country(
                        code=codigo,
                        name=nombre,
                        empresa_reg=suc.empresa,
                        active=activo,
                        user_reg=request.user,
                    )
                    oCountry.save()
                    grupo = {
                        "pk": oCountry.pk,
                        "codigo": oCountry.code,
                        "name": oCountry.name,
                        "activo": oCountry.active,
                    }
                    mensaje = "Se ha guardado el registro del País"
                    data = {"grupo": grupo, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_pais(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                nombre = request.POST["nombre"]
                activo = int(request.POST["activo"])

                if len(nombre) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(nombre) > 150:
                    mensaje = "El campo 'Descripcion' tiene como máximo 150 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oCoun = Country.objects.get(pk=id)
                if oCoun:
                    oCoun.name = nombre
                    oCoun.active = activo
                    oCoun.user_mod = request.user
                    oCoun.date_mod = datetime.now()
                    oCoun.save()
                    country = {
                        "pk": oCoun.pk,
                        "codigo": oCoun.code,
                        "nombre": oCoun.name,
                        "activo": oCoun.active,
                    }
                    mensaje = "Se ha actualizado el registro."
                    data = {"puesto": country, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_pais(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oC = Country.objects.get(pk=reg_id)
                    totReg = Employee.objects.filter(homeCountry__id=reg_id).count()
                    totReg += Employee.objects.filter(workCountry__id=reg_id).count()
                    totReg += Employee.objects.filter(birthCountry__id=reg_id).count()
                    totReg += Employee.objects.filter(citizenship__id=reg_id).count()
                    if oC:
                        if totReg == 0:
                            oC.delete()
                            mensaje = "Se ha eliminado el registro."
                            data = {"mensaje": mensaje, "error": False}
                        else:
                            mensaje = "El registro tiene datos asociados."
                            data = {"mensaje": mensaje, "error": True}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def guardar_deptos(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                codigo = request.POST["codigo"]
                nombre = request.POST["nombre"]
                pais = request.POST["pais"]
                activo = int(request.POST["activo"])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(codigo) == 0:
                    mensaje = "El campo 'Código' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(codigo) > 5:
                    mensaje = "El campo 'Código' tiene como máximo 5 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(nombre) > 150:
                    mensaje = "El campo 'Nombre' tiene como máximo 150 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(pais) == 0:
                    mensaje = "El campo 'País' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if not validarEntero(pais):
                    mensaje = "El valor del campo 'País' no es válido."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if pais == 0:
                    mensaje = "El campo 'País' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])
                pais = Country.objects.get(pk=pais)
                tot_reg = State.objects.filter(
                    code=codigo, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existe un registro con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oDepto = State(
                    code=codigo,
                    name=nombre,
                    empresa_reg=suc.empresa,
                    active=activo,
                    pais=pais,
                    user_reg=request.user,
                )
                oDepto.save()
                grupo = {
                    "pk": oDepto.pk,
                    "code": oDepto.code,
                    "name": oDepto.name,
                    "activo": oDepto.active,
                }
                mensaje = "Se ha guardado el registro"
                data = {"grupo": grupo, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_deptos(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                pais = request.POST["pais"]
                nombre = request.POST["nombre"]
                activo = int(request.POST["activo"])

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(nombre) > 150:
                    mensaje = "El campo 'Nombre' tiene como máximo 150 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(pais) == 0:
                    mensaje = "El campo 'País' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if not validarEntero(pais):
                    mensaje = "El valor del campo 'País' no es válido."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if pais == 0:
                    mensaje = "El campo 'País' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                pais = Country.objects.get(pk=pais)

                oDept = State.objects.get(pk=id)
                if oDept:
                    oDept.name = nombre
                    oDept.pais = pais
                    oDept.active = activo
                    oDept.user_mod = request.user
                    oDept.date_mod = datetime.now()
                    oDept.save()
                    estado = {
                        "pk": oDept.pk,
                        "codigo": oDept.code,
                        "nombre": oDept.name,
                        "activo": oDept.active,
                    }
                    mensaje = "Se ha actualizado el registro."
                    data = {"puesto": estado, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def eliminar_depto(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oS = State.objects.get(pk=reg_id)
                    totReg = Employee.objects.filter(homeState__id=reg_id).count()
                    totReg += Employee.objects.filter(workState__id=reg_id).count()
                    if oS:
                        if totReg == 0:
                            oS.delete()
                            mensaje = "Se ha eliminado el registro."
                            data = {"mensaje": mensaje, "error": False}
                        else:
                            mensaje = "El registro tiene datos asociados."
                            data = {"mensaje": mensaje, "error": True}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_ciudades(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                ID = request.POST["ID"]
                nombre = request.POST["nombre"]
                activo = int(request.POST["activo"])

                if len(ID) > 5:
                    mensaje = "El campo 'Código' tiene un máximo de 5 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                if len(nombre) > 0 and len(ID) > 0:
                    oCdd = Ciudad(
                        code=ID,
                        nombre=nombre,
                        empresa_reg=suc.empresa,
                        active=activo,
                        user_reg=request.user,
                    )
                    oCdd.save()
                    ciudad = {
                        "pk": oCdd.pk,
                        "ID": oCdd.code,
                        "nombre": oCdd.nombre,
                        "activo": oCdd.active,
                    }
                    mensaje = "Se ha guardado el registro"
                    data = {"grupo": ciudad, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_ciudad(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                ID = request.POST["ID"]
                nombre = request.POST["nombre"]
                activo = int(request.POST["activo"])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(ID) > 0 and len(nombre) > 0:
                    oCdd = Ciudad.objects.get(pk=id)
                    if oCdd:
                        oCdd.code = ID
                        oCdd.nombre = nombre
                        oCdd.active = activo
                        oCdd.user_mod = request.user
                        oCdd.date_mod = datetime.now()
                        oCdd.save()
                        ciudad = {
                            "pk": oCdd.pk,
                            "ID": oCdd.code,
                            "nombre": oCdd.nombre,
                            "activo": oCdd.active,
                        }
                        mensaje = "Se ha actualizado el registro."
                        data = {"ciudad": ciudad, "mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_ciudad(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oCdd = Ciudad.objects.get(pk=reg_id)
                    if oCdd:
                        oCdd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_genero(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                code = request.POST["code"]
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(code) == 0:
                    mensaje = 'El campo "Código" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = 'El campo "Código" tiene un máximo de 5 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 25:
                    mensaje = 'El campo "Descripción" tiene un máximo de 25 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])
                tot_reg = Sex.objects.filter(code=code, empresa_reg=suc.empresa).count()
                if tot_reg > 0:
                    mensaje = "Ya existe un registro con el código ingresado"
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oGnr = Sex(
                    code=code,
                    description=desc,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oGnr.save()
                genero = {
                    "pk": oGnr.pk,
                    "code": oGnr.code,
                    "desc": oGnr.description,
                    "activo": oGnr.active,
                }
                mensaje = "Se ha guardado el registro"
                data = {"generos": genero, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def actualizar_genero(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oGnr = Sex.objects.get(pk=id)
                    if oGnr:
                        oGnr.description = desc
                        oGnr.active = activo
                        oGnr.user_mod = request.user
                        oGnr.date_mod = datetime.now()
                        oGnr.save()
                        genero = {
                            "pk": oGnr.pk,
                            "desc": oGnr.description,
                            "activo": oGnr.active,
                        }
                        mensaje = "Se ha actualizado el registro."
                        data = {"ciudad": genero, "mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_genero(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oGnr = Sex.objects.get(pk=reg_id)
                    if oGnr:
                        totReg = Employee.objects.filter(sex__id=reg_id).count()
                        if totReg == 0:
                            oGnr.delete()
                            mensaje = "Se ha eliminado el registro."
                            data = {"mensaje": mensaje, "error": False}
                        else:
                            mensaje = "El registro tiene datos asociados."
                            data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_estado_civil(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                desc = request.POST["desc"]
                code = request.POST["code"]
                activo = int(request.POST["activo"])

                if len(code) == 0:
                    mensaje = "El campo 'Código' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = "El campo 'Código' tiene como máximo 5 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 50:
                    mensaje = "El campo 'Descripción' tiene como máximo 50 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                tot_reg = CivilStatus.objects.filter(
                    empresa_reg=suc.empresa, code=code
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existe un registro con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 0:
                    oCv = CivilStatus(
                        code=code,
                        description=desc,
                        empresa_reg=suc.empresa,
                        active=activo,
                        user_reg=request.user,
                    )
                    oCv.save()
                    estado = {
                        "pk": oCv.pk,
                        "desc": oCv.description,
                        "activo": oCv.active,
                    }
                    mensaje = "Se ha guardado el registro"
                    data = {"estado": estado, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_estado_civil(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 50:
                    mensaje = "El campo 'Descripción' tiene como máximo 50 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oCV = CivilStatus.objects.get(pk=id)
                    if oCV:
                        oCV.description = desc
                        oCV.active = activo
                        oCV.user_mod = request.user
                        oCV.date_mod = datetime.now()
                        oCV.save()
                        estado = {
                            "pk": oCV.pk,
                            "desc": oCV.description,
                            "activo": oCV.active,
                        }
                        mensaje = "Se ha actualizado el registro."
                        data = {"estado": estado, "mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_estado_civil(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oCV = CivilStatus.objects.get(pk=reg_id)
                    if oCV:
                        totReg = Employee.objects.filter(marrStatus__id=reg_id).count()
                        if totReg == 0:
                            oCV.delete()
                            mensaje = "Se ha eliminado el registro."
                            data = {"mensaje": mensaje, "error": False}
                        else:
                            mensaje = "El registro tiene datos asociados."
                            data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_parentesco(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                desc = request.POST["desc"]
                code = request.POST["code"]
                activo = int(request.POST["activo"])

                if len(code) == 0:
                    mensaje = "El campo 'código' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(code) > 5:
                    mensaje = "El campo 'código' tiene como máximo 6 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 50:
                    mensaje = "El campo 'descripción' tiene como máximo 50 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])

                tot_reg = Parentesco.objects.filter(
                    code=code, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existe un registro con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 0:
                    oPr = Parentesco(
                        descripcion=desc,
                        code=code,
                        empresa_reg=suc.empresa,
                        active=activo,
                        user_reg=request.user,
                    )
                    oPr.save()
                    parentesco = {
                        "pk": oPr.pk,
                        "desc": oPr.descripcion,
                        "activo": oPr.active,
                    }
                    mensaje = "Se ha guardado el registro"
                    data = {
                        "parentesco": parentesco,
                        "mensaje": mensaje,
                        "error": False,
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_parentesco(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = "El campo 'descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 50:
                    mensaje = "El campo 'descripción' tiene como máximo 50 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oPr = Parentesco.objects.get(pk=id)
                    if oPr:
                        oPr.descripcion = desc
                        oPr.active = activo
                        oPr.user_mod = request.user
                        oPr.date_mod = datetime.now()
                        oPr.save()
                        parentesco = {
                            "pk": oPr.pk,
                            "desc": oPr.descripcion,
                            "activo": oPr.active,
                        }
                        mensaje = "Se ha actualizado el registro."
                        data = {
                            "parentesco": parentesco,
                            "mensaje": mensaje,
                            "error": False,
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_parentesco(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oPr = Parentesco.objects.get(pk=reg_id)
                    if oPr:
                        oPr.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_funciones(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                desc = request.POST["desc"]
                code = request.POST["code"]
                activo = int(request.POST["activo"])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(code) == 0:
                    mensaje = "El campo 'Código' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = "El campo 'Código' tiene como máximo 5 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 25:
                    mensaje = "El campo 'Descripción' tiene como máximo 25 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])

                tot_reg = FuncionesTrabajo.objects.filter(
                    code=code, empresa_reg=suc.empresa
                ).count()

                if tot_reg > 0:
                    mensaje = "Ya existen registros con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oFn = FuncionesTrabajo(
                    descripcion=desc,
                    code=code,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oFn.save()
                funcion = {
                    "pk": oFn.pk,
                    "code": oFn.code,
                    "desc": oFn.descripcion,
                    "activo": oFn.active,
                }
                mensaje = "Se ha guardado el registro"
                data = {"funcion": funcion, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def actualizar_funcion(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 25:
                    mensaje = "El campo 'Descripción' tiene como máximo 25 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oFn = FuncionesTrabajo.objects.get(pk=id)
                if oFn:
                    oFn.descripcion = desc
                    oFn.active = activo
                    oFn.user_mod = request.user
                    oFn.date_mod = datetime.datetime.now()
                    oFn.save()
                    funcion = {
                        "pk": oFn.pk,
                        "code": oFn.code,
                        "desc": oFn.descripcion,
                        "activo": oFn.active,
                    }
                    mensaje = "Se ha actualizado el registro."
                    data = {"funcion": funcion, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def eliminar_funcion_trabajo(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oFn = FuncionesTrabajo.objects.get(pk=reg_id)
                    if oFn:
                        oFn.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_equipos(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                code = request.POST["code"]
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(code) == 0:
                    mensaje = "El campo 'código' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = "El campo 'código' tiene como máximo 5 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = "El campo 'descripción' tiene como máximo 150 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                tot_reg = EquipoTrabajo.objects.filter(
                    code=code, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existe un registro con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oEq = EquipoTrabajo(
                    code=code,
                    descripcion=desc,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oEq.save()
                equipo = {
                    "pk": oEq.pk,
                    "code": oEq.code,
                    "desc": oEq.descripcion,
                    "activo": oEq.active,
                }
                mensaje = "Se ha guardado el registro"
                data = {"equipo": equipo, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_equipos(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = "El campo 'código' tiene como máximo 5 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = "El campo 'descripción' tiene como máximo 150 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = EquipoTrabajo.objects.get(pk=id)
                if oMd:
                    oMd.descripcion = desc
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    registro = {
                        "pk": oMd.pk,
                        "code": oMd.code,
                        "desc": oMd.descripcion,
                        "activo": oMd.active,
                    }
                    mensaje = "Se ha actualizado el registro."
                    data = {"registro": registro, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_equipo_trabajo(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = EquipoTrabajo.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_estado_empleado(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                nombre = request.POST["nombre"]
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(nombre) == 0:
                    mensaje = "El campo 'Código' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(nombre) > 5:
                    mensaje = "El campo 'Código' tiene como máximo 5 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = "El campo 'Descripción' tiene como máximo 150 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                tot_reg = StatusEmp.objects.filter(
                    code=nombre, empresa_reg=suc.empresa
                ).count()

                if tot_reg > 0:
                    mensaje = "Y xisten registros con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oMd = StatusEmp(
                    code=nombre,
                    description=desc,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    "pk": oMd.pk,
                    "nombre": oMd.code,
                    "desc": oMd.description,
                    "activo": oMd.active,
                }
                mensaje = "Se ha guardado el registro"
                data = {"registro": registro, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_estatus_empleado(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = "El campo 'Descripción' tiene como máximo 150 caracteres."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oMd = StatusEmp.objects.get(pk=id)
                    if oMd:
                        oMd.description = desc
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        registro = {
                            "pk": oMd.pk,
                            "nombre": oMd.code,
                            "desc": oMd.description,
                            "activo": oMd.active,
                        }
                        mensaje = "Se ha actualizado el registro."
                        data = {
                            "registro": registro,
                            "mensaje": mensaje,
                            "error": False,
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_estatus_empleado(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = StatusEmp.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_ausentismo(request):
    oEmp = None
    oAprobo = None
    try:
        if request.is_ajax():
            if request.method == "POST":
                emp = request.POST["emp"]
                desde = request.POST["desde"]
                hasta = request.POST["hasta"]
                motivo = request.POST["motivo"]
                aprobo = request.POST["aprobo"]
                aplica = request.POST["aplica"]
                activo = request.POST["activo"]

                if len(emp) == 0:
                    mensaje = "Seleccione un empleado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    else:
                        mensaje = "Seleccione un empleado."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                if len(desde) == 0:
                    mensaje = "Ingrese una fecha válida en el campo 'Desde'."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(hasta) == 0:
                    mensaje = "Ingrese una fecha válida en el campo 'Hasta'."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(aplica) == 0:
                    mensaje = "Ingrese una fecha válida en el campo 'Fecha que aplica'."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(motivo) == 0:
                    mensaje = "Seleccione un motivo por ausencia."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(motivo) > 0:
                        oMot = MotivosAusencia.objects.get(pk=motivo)
                    else:
                        mensaje = "Seleccione un motivo por ausencia."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                if len(aprobo) == 0:
                    mensaje = "Seleccione el empleado que Aprobó."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(aprobo) > 0:
                        oAprobo = Employee.objects.get(pk=aprobo)

                if int(emp) == int(aprobo):
                    mensaje = "El empleado debe ser distinto al usuario que apruebe."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = Ausentismo(
                    empleado=oEmp,
                    desde=desde,
                    hasta=hasta,
                    motivo=oMot,
                    fecha_aplica=aplica,
                    aprobado=oAprobo,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    "pk": oMd.pk,
                    "empleado": oMd.empleado.pk,
                    "desde": oMd.desde,
                    "hasta": oMd.hasta,
                    "motivo": oMd.motivo.pk,
                    "activo": oMd.active,
                }
                mensaje = "Se ha guardado el registro"
                data = {"registro": registro, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_ausentismo(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                emp = request.POST["emp"]
                desde = request.POST["desde"]
                hasta = request.POST["hasta"]
                motivo = request.POST["motivo"]
                aprobo = request.POST["aprobo"]
                aplica = request.POST["aplica"]
                activo = int(request.POST["activo"])
                oEmp = Employee.objects.get(pk=emp)

                if len(aprobo) > 0:
                    if int(aprobo) > 0:
                        oApro = Employee.objects.get(pk=aprobo)
                    else:
                        oApro = None
                else:
                    oApro = None

                if not oEmp:
                    mensaje = "Ingrese un valor válido como Empleado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                if len(desde) == 0:
                    mensaje = "Ingrese un valor válido en campo 'Desde'."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(hasta) == 0:
                    mensaje = "Ingrese un valor válido en campo 'Hasta'."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(aplica) == 0:
                    mensaje = "Ingrese un valor válido en campo 'Fecha que aplica'."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(motivo) == 0:
                    mensaje = "Seleccione un motivo por ausencia."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(motivo) > 0:
                        oMot = MotivosAusencia.objects.get(pk=motivo)
                    else:
                        mensaje = "Seleccione un motivo por ausencia."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                if int(emp) == int(aprobo):
                    mensaje = "El empleado debe ser distinto al usuario que apruebe."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = Ausentismo.objects.get(pk=id)
                if oMd:
                    oMd.empleado = oEmp
                    oMd.desde = desde
                    oMd.hasta = hasta
                    oMd.motivo = oMot
                    oMd.aprobado = oApro
                    oMd.fecha_aplica = aplica
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    registro = {
                        "pk": oMd.pk,
                        "empleado": oMd.empleado.pk,
                        "desde": oMd.desde,
                        "hasta": oMd.hasta,
                        "motivo": oMd.motivo.pk,
                        "activo": oMd.active,
                    }
                    mensaje = "Se ha actualizado el registro."
                    data = {"registro": registro, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": str(ex),
        }
    return JsonResponse(data)


def eliminar_ausentismo(request):
    try:
        if request.is_ajax():
            print("Entro aqui")
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = Ausentismo.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": str(ex),
        }
    return JsonResponse(data)


def guardar_motivo_ausencia(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                desc = request.POST["desc"]
                code = request.POST["code"]
                pagado = request.POST["pagado"]
                activo = request.POST["activo"]

                if len(code) == 0:
                    mensaje = 'El campo "Código" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "Ingrese una descripción."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = 'El campo "Código" tiene como máximo 5 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = 'El campo "Descripción" tiene como máximo 150 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if int(pagado) == 1:
                    pagado = True
                else:
                    pagado = False

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                tot_reg = MotivosAusencia.objects.filter(
                    code=code, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existen registros con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oMd = MotivosAusencia(
                    code=code,
                    descripcion=desc,
                    pagado=pagado,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    "pk": oMd.pk,
                    "desc": oMd.descripcion,
                    "pagado": oMd.pagado,
                    "activo": oMd.active,
                }
                mensaje = "Se ha guardado el registro"
                data = {"registro": registro, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_motivo_ausencia(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                pagado = request.POST["pagado"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = "Ingrese una descripción."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = 'El campo "Descripción" tiene como máximo 150 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if int(pagado) == 1:
                    pagado = True
                else:
                    pagado = False

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = MotivosAusencia.objects.get(pk=id)
                if oMd:
                    oMd.descripcion = desc
                    oMd.pagado = pagado
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    registro = {
                        "pk": oMd.pk,
                        "descripcion": oMd.descripcion,
                        "pagado": oMd.pagado,
                        "activo": oMd.active,
                    }
                    mensaje = "Se ha actualizado el registro."
                    data = {"registro": registro, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_motivo_ausencia(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = MotivosAusencia.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def guardar_motivo_despido(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                desc = request.POST["desc"]
                code = request.POST["code"]
                activo = request.POST["activo"]

                if len(code) == 0:
                    mensaje = 'El campo "Código" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = 'El campo "Código" tiene como máximo 5 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(code) > 150:
                    mensaje = 'El campo "Descripción" tiene como máximo 150 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                tot_reg = MotivosDespido.objects.filter(
                    code=code, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existen registros con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oMd = MotivosDespido(
                    descripcion=desc,
                    empresa_reg=suc.empresa,
                    code=code,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    "pk": oMd.pk,
                    "desc": oMd.descripcion,
                    "code": oMd.code,
                    "activo": oMd.active,
                }
                mensaje = "Se ha guardado el registro"
                data = {"registro": registro, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_motivo_despido(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = 'El campo "Descripción" tiene como máximo 150 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oMd = MotivosDespido.objects.get(pk=id)
                    if oMd:
                        oMd.descripcion = desc
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        registro = {
                            "pk": oMd.pk,
                            "descripcion": oMd.descripcion,
                            "code": oMd.code,
                            "activo": oMd.active,
                        }
                        mensaje = "Se ha actualizado el registro."
                        data = {
                            "registro": registro,
                            "mensaje": mensaje,
                            "error": False,
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_motivo_despido(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = MotivosDespido.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_motivo_renuncia(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                desc = request.POST["desc"]
                code = request.POST["code"]
                activo = request.POST["activo"]

                if len(code) == 0:
                    mensaje = 'El campo "Código" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = 'El campo "Código" tiene como máximo 5 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = 'El campo "Descripción" tiene como máximo 150 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                tot_reg = MotivosRenuncia.objects.filter(
                    code=code, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existen registros con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oMd = MotivosRenuncia(
                    code=code,
                    descripcion=desc,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    "pk": oMd.pk,
                    "code": oMd.code,
                    "desc": oMd.descripcion,
                    "activo": oMd.active,
                }
                mensaje = "Se ha guardado el registro"
                data = {"registro": registro, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_motivo_renuncia(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = 'El campo "Descripción" tiene como máximo 150 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oMd = MotivosRenuncia.objects.get(pk=id)
                    if oMd:
                        oMd.descripcion = desc
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        registro = {
                            "pk": oMd.pk,
                            "code": oMd.code,
                            "descripcion": oMd.descripcion,
                            "activo": oMd.active,
                        }
                        mensaje = "Se ha actualizado el registro."
                        data = {
                            "registro": registro,
                            "mensaje": mensaje,
                            "error": False,
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_motivo_renuncia(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = MotivosRenuncia.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_clase_educacion(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                code = request.POST["code"]
                desc = request.POST["desc"]
                activo = request.POST["activo"]

                if len(code) == 0:
                    mensaje = 'El campo "Código" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = 'El campo "Código" es tiene como máximo 5 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = ClaseEducacion(
                    code=code,
                    descripcion=desc,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    "pk": oMd.pk,
                    "codigo": oMd.code,
                    "desc": oMd.descripcion,
                    "activo": oMd.active,
                }
                mensaje = "Se ha guardado el registro"
                data = {"registro": registro, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_clase_educacion(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                code = request.POST["code"]
                activo = int(request.POST["activo"])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0 and len(code) > 0:
                    oMd = ClaseEducacion.objects.get(pk=id)
                    if oMd:
                        oMd.code = code
                        oMd.descripcion = desc
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        registro = {
                            "pk": oMd.pk,
                            "code": oMd.code,
                            "descripcion": oMd.descripcion,
                            "activo": oMd.active,
                        }
                        mensaje = "Se ha actualizado el registro."
                        data = {
                            "registro": registro,
                            "mensaje": mensaje,
                            "error": False,
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_clase_educacion(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = ClaseEducacion.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_educacion(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                emp = request.POST["emp"]
                formacion = request.POST["formacion"]
                desde = request.POST["desde"]
                hasta = request.POST["hasta"]
                entidad = request.POST["entidad"]
                asignatura = request.POST["asignatura"]
                titulo = request.POST["titulo"]

                if len(emp) == 0:
                    mensaje = "Seleccione un empleado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    else:
                        mensaje = "Seleccione un empleado."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                if len(formacion) == 0:
                    mensaje = "Seleccione una Clase de Formación."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(formacion) > 0:
                        oClsEdu = ClaseEducacion.objects.get(pk=formacion)
                    else:
                        mensaje = "Seleccione una Clase de Formación."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                if len(desde) == 0:
                    mensaje = 'El campo "Desde" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(hasta) == 0:
                    mensaje = 'El campo "Hasta" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(entidad) == 0:
                    mensaje = 'El campo "Institución" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(asignatura) == 0:
                    mensaje = 'El campo "Asignatura Principal" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(titulo) == 0:
                    mensaje = 'El campo "Título" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = Educacion(
                    empleado=oEmp,
                    clase_edu=oClsEdu,
                    desde=desde,
                    hasta=hasta,
                    entidad=entidad,
                    asignatura_principal=asignatura,
                    titulo=titulo,
                    empresa_reg=suc.empresa,
                    active=True,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    "pk": oMd.pk,
                    "emp": oMd.empleado.pk,
                    "clase_edu": oMd.clase_edu.pk,
                    "desde": oMd.desde,
                    "hasta": oMd.hasta,
                    "entidad": oMd.entidad,
                    "asignatura": oMd.asignatura_principal,
                    "titulo": oMd.titulo,
                    "activo": oMd.active,
                }
                mensaje = "Se ha guardado el registro"
                data = {"registro": registro, "mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_educacion(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                emp = request.POST["emp"]
                formacion = request.POST["formacion"]
                desde = request.POST["desde"]
                hasta = request.POST["hasta"]
                entidad = request.POST["entidad"]
                asignatura = request.POST["asignatura"]
                titulo = request.POST["titulo"]

                if len(emp) == 0:
                    mensaje = "Seleccione un empleado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    else:
                        mensaje = "Seleccione un empleado."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                if len(formacion) == 0:
                    mensaje = "Seleccione una Clase de Formación."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(formacion) > 0:
                        oClsEdu = ClaseEducacion.objects.get(pk=formacion)
                    else:
                        mensaje = "Seleccione una Clase de Formación."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                if len(desde) == 0:
                    mensaje = 'El campo "Desde" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(hasta) == 0:
                    mensaje = 'El campo "Hasta" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(entidad) == 0:
                    mensaje = 'El campo "Institución" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(asignatura) == 0:
                    mensaje = 'El campo "Asignatura Principal" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(titulo) == 0:
                    mensaje = 'El campo "Título" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oMd = Educacion.objects.get(pk=id)
                if oMd:
                    oMd.empleado = oEmp
                    oMd.clase_edu = oClsEdu
                    oMd.desde = desde
                    oMd.hasta = hasta
                    oMd.entidad = entidad
                    oMd.asignatura_principal = asignatura
                    oMd.titulo = titulo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    registro = {
                        "pk": oMd.pk,
                        "empleado": oMd.empleado.pk,
                        "clase_educacion": oMd.clase_edu.pk,
                        "desde": oMd.desde,
                        "hasta": oMd.hasta,
                        "entidad": oMd.entidad,
                        "asignatura": oMd.asignatura_principal,
                        "titulo": oMd.titulo,
                    }
                    mensaje = "Se ha actualizado el registro."
                    data = {"registro": registro, "mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_educacion(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = Educacion.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_evaluacion(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                emp = request.POST["emp"]
                gerente = request.POST["gerente"]
                fecha = request.POST["fecha"]
                grupo_asal = request.POST["grupo_asal"]
                desc = request.POST["desc"]
                coment = request.POST["coment"]
                oGerente = None

                if len(emp) == 0:
                    mensaje = "Seleccione un empleado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    elif int(emp) == 0:
                        mensaje = "Seleccione un empleado."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)
                    else:
                        mensaje = "Empleado no existe."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                if len(gerente) > 0:
                    if int(gerente) > 0:
                        oGerente = Employee.objects.get(pk=gerente)

                if int(emp) == int(gerente):
                    data = {
                        "mensaje": "El campo empleado no puede ser la misma opción que el gerente.",
                        "error": True,
                    }
                    return JsonResponse(data)

                if len(fecha) == 0:
                    mensaje = 'El campo "Fecha" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(grupo_asal) == 0:
                    mensaje = 'El campo "Grupo asalariado" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(coment) == 0:
                    mensaje = 'El campo "Comentario" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = Evaluacion(
                    empleado=oEmp,
                    gerente=oGerente,
                    fecha=fecha,
                    grupo_salarial=grupo_asal,
                    descripcion=desc,
                    comentario=coment,
                    empresa_reg=suc.empresa,
                    active=True,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_evaluacion(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                emp = request.POST["emp"]
                gerente = request.POST["gerente"]
                fecha = request.POST["fecha"]
                grupo_asal = request.POST["grupo_asal"]
                desc = request.POST["desc"]
                coment = request.POST["coment"]

                if len(emp) == 0:
                    mensaje = "Seleccione un empleado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    elif int(emp) == 0:
                        mensaje = "Seleccione un empleado."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)
                    else:
                        mensaje = "Empleado no existe."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                if len(gerente) > 0:
                    if int(gerente) > 0:
                        oGerente = Employee.objects.get(pk=gerente)

                if int(emp) == int(gerente):
                    data = {
                        "mensaje": "El campo empleado no puede ser la misma opción que el gerente.",
                        "error": True,
                    }
                    return JsonResponse(data)

                if len(fecha) == 0:
                    mensaje = 'El campo "Fecha" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(grupo_asal) == 0:
                    mensaje = 'El campo "Grupo asalariado" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(coment) == 0:
                    mensaje = 'El campo "Comentario" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oEmple = Employee.objects.get(pk=int(emp))
                oGerent = Employee.objects.get(pk=gerente)
                oMd = Evaluacion.objects.get(pk=id)
                if oMd:
                    oMd.empleado = oEmple
                    oMd.gerente = oGerent
                    oMd.fecha = fecha
                    oMd.grupo_salarial = grupo_asal
                    oMd.descripcion = desc
                    oMd.comentario = coment
                    oMd.active = True
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def eliminar_evaluacion(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = Evaluacion.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_motivo_aumento_sueldo(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                desc = request.POST["desc"]
                code = request.POST["code"]
                activo = request.POST["activo"]

                if len(code) == 0:
                    mensaje = 'El campo "Código" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = 'El campo "Código" tiene como máximo 5 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = 'El campo "Descripción" tiene como máximo 150 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                tot_reg = MotivoAumentoSueldo.objects.filter(
                    code=code, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existe un registro con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oMd = MotivoAumentoSueldo(
                    code=code,
                    descripcion=desc,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def actualizar_motivo_aumento_sueldo(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = 'El campo "Descripción" tiene como máximo 150 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = MotivoAumentoSueldo.objects.get(pk=id)
                if oMd:
                    oMd.descripcion = desc
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_motivo_aumento_sueldo(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = MotivoAumentoSueldo.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def guardar_motivo_rescision_contrato(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                nombre = request.POST["nombre"]
                desc = request.POST["desc"]
                activo = request.POST["activo"]

                if len(nombre) == 0:
                    mensaje = 'El campo "código" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(nombre) > 5:
                    mensaje = 'El campo "código" tiene como máximo de 5 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = 'El campo "Descripción" tiene como máximo 150 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                tot_reg = TermReason.objects.filter(
                    code=nombre, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existen registros con el código ingresado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                oMd = TermReason(
                    code=nombre,
                    description=desc,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_motivo_rescision_contrato(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = 'El campo "Descripción" tiene como máximo 150 caracteres.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = TermReason.objects.get(pk=id)
                if oMd:
                    oMd.description = desc
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_motivo_rescision_contrato(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = TermReason.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_empleo_anterior(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                emp = request.POST["emp"]
                desde = request.POST["desde"]
                hasta = request.POST["hasta"]
                empresa = request.POST["empresa"]
                posicion = request.POST["posicion"]
                comentario = request.POST["comentario"]
                activo = request.POST["activo"]

                if len(emp) == 0:
                    mensaje = "Seleccione un empleado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    elif int(emp) == 0:
                        mensaje = "Seleccione un empleado."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)
                    else:
                        mensaje = "Empleado no existe."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                if len(desde) == 0:
                    mensaje = 'El campo "Desde" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(hasta) == 0:
                    mensaje = 'El campo "Hasta" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(empresa) == 0:
                    mensaje = 'El campo "Empresa" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(posicion) == 0:
                    mensaje = 'El campo "Posición" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                oMd = EmpleosAnteriores(
                    empleado=oEmp,
                    desde=desde,
                    hasta=hasta,
                    empresa=empresa,
                    posicion=posicion,
                    comentario=comentario,
                    user_reg=request.user,
                    active=activo,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_empleo_anterior(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                emp = request.POST["emp"]
                desde = request.POST["desde"]
                hasta = request.POST["hasta"]
                empresa = request.POST["empresa"]
                posicion = request.POST["posicion"]
                comentario = request.POST["comentario"]
                activo = request.POST["activo"]
                oEmp = None

                if len(emp) == 0:
                    mensaje = "Seleccione un empleado."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    elif int(emp) == 0:
                        mensaje = "Seleccione un empleado."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)
                    else:
                        mensaje = "Empleado no existe."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                if len(desde) == 0:
                    mensaje = 'El campo "Desde" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(hasta) == 0:
                    mensaje = 'El campo "Hasta" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(empresa) == 0:
                    mensaje = 'El campo "Empresa" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if len(posicion) == 0:
                    mensaje = 'El campo "Posición" es obligatorio.'
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                oMd = EmpleosAnteriores.objects.get(pk=id)
                if oMd:
                    oMd.empleado = oEmp
                    oMd.desde = desde
                    oMd.hasta = hasta
                    oMd.empresa = empresa
                    oMd.posicion = posicion
                    oMd.comentario = comentario
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_empleo_anterior(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = EmpleosAnteriores.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_grupo_comision(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                desc = request.POST["desc"]
                code = request.POST["code"]
                activo = request.POST["activo"]

                if len(code) == 0:
                    mensaje = 'El campo "Código" es obligatorio.'
                    data = {
                        "mensaje": mensaje,
                        "error": True,
                    }
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {
                        "mensaje": mensaje,
                        "error": True,
                    }
                    return JsonResponse(data)

                if len(code) == 0:
                    mensaje = 'El campo "Código" tiene como máximo 5 caracteres.'
                    data = {
                        "mensaje": mensaje,
                        "error": True,
                    }
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])

                tot_reg = GrupoComisiones.objects.filter(
                    code=code, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existen registros con el código ingresado."
                    data = {
                        "mensaje": mensaje,
                        "error": True,
                    }
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                oMd = GrupoComisiones(
                    descripcion=desc,
                    code=code,
                    empresa_reg=suc.empresa,
                    active=True,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def actualizar_grupo_comision(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc1 = request.POST["desc"]
                activo1 = request.POST["activo"]
                acti = False

                if len(desc1) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {
                        "mensaje": mensaje,
                        "error": False,
                    }

                if int(activo1) == 1:
                    acti = True
                else:
                    acti = False

                oMd = GrupoComisiones.objects.get(pk=id)
                if oMd:
                    oMd.descripcion = desc1
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.active = acti
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_grupo_comision(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = GrupoComisiones.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_vendedor(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                nombre = request.POST["nombre"]
                grp_com = request.POST["grupo_com"]
                porcent = request.POST["porcentaje"]
                # emp = request.POST['emp']
                tel = request.POST["tel"]
                movil = request.POST["movil"]
                correo = request.POST["correo"]
                coment = request.POST["coment"]
                activo = int(request.POST["activo"])
                oGrpCom = None
                vPorcentajeComision = 0

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(grp_com) == 0:
                    mensaje = "El campo 'Grupo de Comisión' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)
                else:
                    if int(grp_com) > 0:
                        oGrpCom = GrupoComisiones.objects.get(pk=grp_com)

                if len(porcent) > 0:
                    vPorcentajeComision = porcent

                # if len(emp) == 0:
                #     mensaje = 'Seleccione un empleado.'
                #     data = {
                #         'mensaje': mensaje, 'error': True
                #     }
                #     return JsonResponse(data)
                # else:
                #     if int(emp) > 0:
                #         oEmp = Employee.objects.get(pk=emp)
                #     elif int(emp) == 0:
                #         mensaje = 'Seleccione un empleado.'
                #         data = {
                #             'mensaje': mensaje, 'error': True
                #         }
                #         return JsonResponse(data)
                #     else:
                #         mensaje = 'Empleado no existe.'
                #         data = {
                #             'mensaje': mensaje, 'error': True
                #         }
                #         return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = Vendedor(
                    nombre=nombre,
                    grupo_comisiones=oGrpCom,
                    porcentaje_comision=float(vPorcentajeComision),
                    # empleado=oEmp,
                    telefono=tel,
                    tel_movil=movil,
                    correo=correo,
                    comentario=coment,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()

                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def actualizar_vendedor(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                nombre = request.POST["nombre"]
                grp_com = request.POST["grupo_com"]
                porcent = request.POST["porcentaje"]
                # emp = request.POST['emp']
                tel = request.POST["tel"]
                movil = request.POST["movil"]
                correo = request.POST["correo"]
                coment = request.POST["coment"]
                activo = int(request.POST["activo"])
                vPorcentajeComision = 0.00
                oGrpCom = []

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(grp_com) == 0:
                    mensaje = "El campo 'Grupo de Comisión' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)
                else:
                    if int(grp_com) > 0:
                        oGrpCom = GrupoComisiones.objects.get(pk=grp_com)

                if len(porcent) > 0:
                    vPorcentajeComision = porcent

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = Vendedor.objects.get(pk=id)
                if oMd:
                    oMd.nombre = nombre
                    oMd.grupo_com = oGrpCom
                    oMd.porcentaje_comision = vPorcentajeComision
                    oMd.grupo_comision = oGrpCom
                    oMd.telefono = tel
                    oMd.tel_movil = movil
                    oMd.correo = correo
                    oMd.comentario = coment
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
    return JsonResponse(data)


def eliminar_vendedor(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = Vendedor.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_feriado(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                fecha = request.POST["fecha"]
                rate = request.POST["rate"]
                comentario = request.POST["comentario"]
                activo = int(request.POST["activo"])

                if len(fecha) == 0:
                    mensaje = "El campo 'Fecha' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(rate) == 0:
                    mensaje = "El campo 'Rate' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(comentario) == 0:
                    mensaje = "El campo 'Comentario' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(rate) > 10:
                    mensaje = "El campo 'Rate' tiene como máximo 10 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(comentario) > 150:
                    mensaje = "El campo 'Comentario' tiene como máximo 150 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                tot_reg = Feriado.objects.filter(
                    fecha=fecha, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existe un registro de feriado con la fecha ingresada."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                oMd = Feriado(
                    fecha=fecha,
                    rate=rate,
                    empresa_reg=suc.empresa,
                    descripcion=comentario,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_feriado(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                fecha = request.POST["fecha"]
                rate = request.POST["rate"]
                comentario = request.POST["comentario"]
                activo = int(request.POST["activo"])

                if len(fecha) == 0:
                    mensaje = "El campo 'Fecha' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(rate) == 0:
                    mensaje = "El campo 'Rate' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(comentario) == 0:
                    mensaje = "El campo 'Comentario' es obligatorio."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = Feriado.objects.get(pk=id)
                if oMd:
                    oMd.fecha = fecha
                    oMd.rate = rate
                    oMd.comentario = comentario
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_feriado(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = Feriado.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_activo_asignado(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                code = request.POST["code"]
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(code) == 0:
                    mensaje = "El campo 'Código' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])
                tot_reg = ActivoAsignado.objects.filter(
                    code=code, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existe un registro con el código ingresado."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                tot_reg = ActivoAsignado.objects.filter(
                    descripcion=desc, empresa_reg=suc.empresa
                ).count()
                if tot_reg > 0:
                    mensaje = "Ya existe un registro con la descripción ingresada."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = ActivoAsignado(
                    code=code,
                    descripcion=desc,
                    active=activo,
                    empresa_reg=suc.empresa,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_activo_asignado(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                code = request.POST["code"]
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = ActivoAsignado.objects.get(pk=id)
                if oMd:
                    oMd.descripcion = desc
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = timezone.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_activo_asignado(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = ActivoAsignado.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_tipo_salario(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                nombre = request.POST["nombre"]
                desc = request.POST["desc"]
                dias = request.POST["dias"]
                activo = int(request.POST["activo"])

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(nombre) > 5:
                    mensaje = "El campo 'Código' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if validarEntero(dias) != True:
                    mensaje = "El campo 'Días de salario' es de tipo numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = SalaryUnit(
                    code=nombre,
                    description=desc,
                    empresa_reg=suc.empresa,
                    dias_salario=dias,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_tipo_salario(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                nombre = request.POST["nombre"]
                dias = request.POST["dias"]
                activo = int(request.POST["activo"])

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if validarEntero(dias) != True:
                    mensaje = "El campo 'Dias de salario' es de tipo numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = SalaryUnit.objects.get(pk=id)
                if oMd:
                    oMd.description = desc
                    oMd.code = nombre
                    oMd.dias_salario = dias
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_tipo_salario(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = SalaryUnit.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_costo_empleado(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                nombre = request.POST["nombre"]
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(nombre) == 0:
                    mensaje = "El campo 'Código' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(nombre) > 5:
                    mensaje = "El campo 'Código' tiene un máximo de 5 carateres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = "El campo 'Descripción' tiene un máximo de 150 carateres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                tot_reg = CostUnit.objects.filter(
                    code=nombre, empresa_reg=suc.empresa
                ).count()

                if tot_reg > 0:
                    mensaje = "Ya existe un registro con el código ingresado."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                oMd = CostUnit(
                    code=nombre,
                    description=desc,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_costo_empleado(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) > 150:
                    mensaje = "El campo 'Descripción' tiene como máximo 150 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = CostUnit.objects.get(pk=id)
                if oMd:
                    oMd.description = desc
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_costo_empleado(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = CostUnit.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def guardar_banco(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                nombre = request.POST["nombre"]
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(nombre) == 0:
                    mensaje = "El campo 'Código' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(nombre) > 5:
                    mensaje = "El campo 'Código' tiene como máximo 5 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = Bank(
                    code=nombre,
                    description=desc,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_banco(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desc = request.POST["desc"]
                activo = int(request.POST["activo"])

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = Bank.objects.get(pk=id)
                if oMd:
                    oMd.description = desc
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": str(ex),
        }
    return JsonResponse(data)


def eliminar_banco(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = Bank.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": str(ex),
        }
    return JsonResponse(data)


def guardar_empresa_usuario(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                empresa = request.POST["empresa"]
                usuario = request.POST["usuario"]
                activo = int(request.POST["activo"])

                if len(empresa) == 0:
                    mensaje = "Seleccione una empresa."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(empresa) > 0:
                        oEmpresa = Empresa.objects.get(pk=empresa)
                    elif int(empresa) == 0:
                        mensaje = "Seleccione una empresa."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)
                    else:
                        mensaje = "Empleado no existe."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                if len(usuario) == 0:
                    mensaje = "Seleccione un usuario."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(usuario) > 0:
                        oUsuario = User.objects.get(pk=usuario)
                    elif int(usuario) == 0:
                        mensaje = "Seleccione un usuario."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)
                    else:
                        mensaje = "Empleado no existe."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                cReg = UsuarioEmpresa.objects.filter(
                    empresa=oEmpresa, usuario=oUsuario
                ).count()

                if cReg > 0:
                    mensaje = "La empresa ya está asociada al usuario"
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = UsuarioEmpresa(
                    empresa=oEmpresa,
                    usuario=oUsuario,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def actualizar_empresa_usuario(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                empresa = request.POST["empresa"]
                usuario = request.POST["usuario"]
                activo = int(request.POST["activo"])

                if len(empresa) == 0:
                    mensaje = "Seleccione una empresa."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(empresa) > 0:
                        oEmpresa = Empresa.objects.get(pk=empresa)
                    elif int(empresa) == 0:
                        mensaje = "Seleccione una empresa."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)
                    else:
                        mensaje = "Empleado no existe."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                if len(usuario) == 0:
                    mensaje = "Seleccione un usuario."
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)
                else:
                    if int(usuario) > 0:
                        oUsuario = User.objects.get(pk=usuario)
                    elif int(usuario) == 0:
                        mensaje = "Seleccione un usuario."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)
                    else:
                        mensaje = "Usuario no existe."
                        data = {"mensaje": mensaje, "error": True}
                        return JsonResponse(data)

                cReg = UsuarioEmpresa.objects.filter(
                    empresa=oEmpresa, usuario=oUsuario
                ).exclude(pk=id)

                if cReg.count() > 0:
                    mensaje = "La empresa ya está asociada al usuario"
                    data = {"mensaje": mensaje, "error": True}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = UsuarioEmpresa.objects.get(pk=id)
                if oMd:
                    oMd.empresa = oEmpresa
                    oMd.usuario = oUsuario
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def eliminar_empresa_usuario(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = UsuarioEmpresa.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def lista_sucursal(request):
    sucursales = None
    idEmpresa = request.GET.get("idEmpresa")
    sucursales_flat = UsuarioSucursal.objects.filter(
        usuario=request.user, sucursal__empresa__id=idEmpresa
    ).values_list("sucursal__id", flat=True)
    sucursales = Branch.objects.filter(pk__in=sucursales_flat)
    data = {"pk": idEmpresa}
    # return JsonResponse(data)
    return render(request, "ajax/lista_sucursales.html", {"sucursales": sucursales})


def lista_estados(request):
    estados = None
    idPais = request.GET.get("idPais")
    estados = State.objects.filter(pais__id=idPais, active=True)
    return render(request, "ajax/lista_estados.html.", {"estados": estados})


def guardar_foto_perfil(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                empleado_id = request.POST["empleado"]
                tot_reg = ImagenEmpleado.objects.filter(
                    empleado__id=empleado_id
                ).count()
                if tot_reg > 0:
                    instancia = ImagenEmpleado.objects.get(empleado__id=empleado_id)
                    form = ImagenEmpleadoForm(
                        request.POST, request.FILES, instance=instancia
                    )
                    # data = serializers.serialize("json", [instancia,])
                    # data = data.strip("[]")
                else:
                    form = ImagenEmpleadoForm(request.POST, request.FILES)

                if form.is_valid():
                    form.save()
                    instancia = ImagenEmpleado.objects.get(empleado__id=empleado_id)
                    return render(
                        request, "ajax/imagen-perfil.html", {"imagen": instancia}
                    )
                    # return JsonResponse({'error': False, 'mensaje': 'Se han cargado los datos'})
                else:
                    return JsonResponse({"error": True, "errors": form.errors})
            else:
                # form = ImagenEmpleadoForm()
                return JsonResponse(
                    {"error": True, "mensaje": "El método no esta permitido"}
                )
        else:
            return JsonResponse({"error": True, "mensaje": "El método no es asíncrono"})
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
        return JsonResponse(data)


def enviar_sucursal(request):
    try:
        if request.is_ajax():
            IdSucursal = request.GET.get("idSucursal")
            totreg = Branch.objects.filter(pk=IdSucursal).count()
            if totreg > 0:
                sucursal = Branch.objects.get(pk=IdSucursal)
                request.session["nombre_sucursal"] = sucursal.description
                request.session["sucursal"] = IdSucursal
                return JsonResponse({"error": False, "mensaje": "Sucursal válida"})
            else:
                request.session["sucursal"] = 0
                request.session["nombre_sucursal"] = ""
                return JsonResponse(
                    {"error": True, "mensaje": "El método no es asíncrono"}
                )
        else:
            return JsonResponse({"error": True, "mensaje": "El método no es asíncrono"})
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
        return JsonResponse(data)


def obtener_ultimo_salario(request):
    try:
        if request.is_ajax():
            IdEmpleado = request.GET.get("idEmpleado")
            aumentos = IncrementosSalariales.objects.filter(
                empleado__pk=IdEmpleado
            ).order_by("-fecha_incremento")
            if aumentos.count() > 0:
                o_aumento = aumentos[0]
                return JsonResponse(
                    {
                        "error": False,
                        "mensaje": "Respuesta exitosa",
                        "salario_anterior": o_aumento.nuevo_salario,
                    }
                )
            else:
                return JsonResponse(
                    {
                        "error": False,
                        "mensaje": "Respuesta exitosa",
                        "salario_anterior": 0.00,
                    }
                )
        else:
            return JsonResponse({"error": True, "mensaje": "El método no es asíncrono"})
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex,
        }
        return JsonResponse(data)


def grafico1(request):
    ldeptos = []
    ltotalemp = []
    try:
        if request.is_ajax():
            suc = Branch.objects.get(pk=request.session["sucursal"])
            deptos = Department.objects.filter(empresa_reg=suc.empresa)
            for item in deptos:
                tot_emp = 0
                tot_emp = Employee.objects.filter(dept=item, branch=suc).count()
                ldeptos.append(item.description)
                ltotalemp.append(tot_emp)

            return JsonResponse(
                {
                    "error": False,
                    "mensaje": "Se obtuvieron los datos",
                    "departamentos": ldeptos,
                    "total_emp": ltotalemp,
                }
            )
        else:
            return JsonResponse({"error": True, "mensaje": "El método no es asíncrono"})
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": "ex",
        }
        return JsonResponse(data)


# region Codigo para Aumento de Sueldo


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_incrementossalariales", raise_exception=True)
def aumento_salario_listado(request):
    lista = []
    busqueda = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(empresa_reg=suc.empresa, branch=suc)
    motivos_aumento = MotivoAumentoSueldo.objects.filter(empresa_reg=suc.empresa)
    if "empleado" in request.GET:
        emp = request.GET.get("empleado")
        if len(emp) > 0:
            if int(emp) > 0:
                busqueda = int(emp)
                empleado = Employee.objects.get(pk=busqueda)
                lista = IncrementosSalariales.objects.filter(
                    empleado=empleado, empresa_reg=suc.empresa, empleado__branch=suc
                )
            else:
                lista = IncrementosSalariales.objects.filter(
                    empresa_reg=suc.empresa, empleado__branch=suc
                )
    else:
        lista = IncrementosSalariales.objects.filter(
            empresa_reg=suc.empresa, empleado__branch=suc
        )

    # suc = Branch.objects.get(pk=request.session["sucursal"])
    # empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(
        request,
        "aumento-salario-listado.html",
        {
            "empleados": empleados,
            "datos": lista,
            "busqueda": busqueda,
            "motivos": motivos_aumento,
        },
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_incrementossalariales", raise_exception=True)
def aumento_salario_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(
        active=True, empresa_reg=suc.empresa, branch=suc
    )
    motivos = MotivoAumentoSueldo.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(
        request,
        "aumento-salario-form.html",
        {"empleados": empleados, "motivos": motivos},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_incrementossalariales", raise_exception=True)
def aumento_salario_editar(request, id):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    motivos = MotivoAumentoSueldo.objects.filter(active=True, empresa_reg=suc.empresa)
    dato = IncrementosSalariales.objects.get(pk=id)
    dato = {
        "pk": dato.pk,
        "empleado": dato.empleado,
        "fecha_incremento": dato.fecha_incremento,
        "motivo_aumento": dato.motivo_aumento,
        "salario_anterior": locale.format("%.2f", dato.salario_anterior, grouping=True),
        "incremento": locale.format("%.2f", dato.incremento, grouping=True),
        "nuevo_salario": locale.format("%.2f", dato.nuevo_salario, grouping=True),
        "comentarios": dato.comentarios,
    }
    return render(
        request,
        "aumento-salario-form.html",
        {"empleados": empleados, "dato": dato, "motivos": motivos, "editar": True},
    )


# ------------------ AJAX -----------------------


def aumento_salario_guardar(request):
    fecha_incremento = ""
    salario_anterior = 0.00
    incremento = 0.00
    nuevo_salario = 0.00
    try:
        if request.is_ajax():
            if request.method == "POST":
                empleado_fk = request.POST["empleado_fk"]
                fecha_incremento = request.POST["fecha_incremento"]
                motivo_aumento_fk = request.POST["motivo_aumento"]
                salario_anterior = request.POST["salario_anterior"]
                incremento = request.POST["incremento"]
                nuevo_salario = request.POST["nuevo_salario"]
                comentarios = request.POST["comentarios"]
                if int(empleado_fk) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "empleado" es obligatorio.',
                        }
                    )
                else:
                    empleados = Employee.objects.filter(pk=empleado_fk)
                    if empleados.count() > 0:
                        o_empleado = Employee.objects.get(pk=empleado_fk)
                    else:
                        return JsonResponse(
                            {"error": True, "mensaje": "El empleado no existe."}
                        )

                if len(fecha_incremento) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Fecha de Incremento" es obligatorio.',
                        }
                    )

                if motivo_aumento_fk == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "motivo de aumento" es obligatorio.',
                        }
                    )
                else:
                    motivos = MotivoAumentoSueldo.objects.filter(pk=motivo_aumento_fk)
                    if motivos.count() > 0:
                        o_motivo = MotivoAumentoSueldo.objects.get(pk=motivo_aumento_fk)
                    else:
                        return JsonResponse(
                            {
                                "error": True,
                                "mensaje": 'El "motivo de aumento" no existe.',
                            }
                        )

                fecha_incremento = datetime.datetime.strptime(fecha_incremento, "%d/%m/%Y")
                fecha_incremento = datetime.datetime.strftime(fecha_incremento, "%Y-%m-%d")
                aumentos = IncrementosSalariales.objects.filter(
                    empleado=o_empleado, fecha_incremento=fecha_incremento
                )

                if aumentos.count() > 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": "Ya existe un registro de aumento para el empleado en la fecha seleccionada.",
                        }
                    )

                if validarDecimal(incremento) == False:
                    return JsonResponse(
                        {"error": True, "mensaje": "El tipo de dato no es válido."}
                    )
                else:
                    if incremento == 0:
                        return JsonResponse(
                            {
                                "error": True,
                                "mensaje": "El incremento tiene que ser mayor a cero.",
                            }
                        )

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oIncremento = IncrementosSalariales(
                    empleado=o_empleado,
                    fecha_incremento=fecha_incremento,
                    motivo_aumento=o_motivo,
                    salario_anterior=salario_anterior,
                    incremento=incremento,
                    nuevo_salario=nuevo_salario,
                    comentarios=comentarios,
                    salario_actual=True,
                    empresa_reg=suc.empresa,
                    user_reg=request.user,
                    active=True,
                )
                oIncremento.save()
                return JsonResponse(
                    {
                        "error": False,
                        "mensaje": "Se ha guardado el registro de Aumento de salario.",
                    }
                )
            else:
                return JsonResponse(
                    {"error": True, "mensaje": "El método no está permitido."}
                )
        else:
            pass
        return JsonResponse({"error": False, "mensaje": "Respuesta exitosa"})
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": str(ex),
        }
        return JsonResponse(data)


def aumento_salario_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = request.POST["reg_id"]
                motivo = request.POST["motivo"]
                incremento = request.POST["incremento"]
                comentarios = request.POST["comentarios"]

                if motivo == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "motivo de aumento" es obligatorio.',
                        }
                    )
                else:
                    motivos = MotivoAumentoSueldo.objects.filter(pk=motivo)
                    if motivos.count() > 0:
                        o_motivo = MotivoAumentoSueldo.objects.get(pk=motivo)
                    else:
                        return JsonResponse(
                            {
                                "error": True,
                                "mensaje": 'El "motivo de aumento" no existe.',
                            }
                        )

                if validarDecimal(incremento) == False:
                    return JsonResponse(
                        {"error": True, "mensaje": "El tipo de dato no es válido."}
                    )
                else:
                    if incremento == 0:
                        return JsonResponse(
                            {
                                "error": True,
                                "mensaje": "El incremento tiene que ser mayor a cero.",
                            }
                        )

                tot_reg = IncrementosSalariales.objects.filter(pk=id).count()
                if tot_reg > 0:
                    o_Incremento = IncrementosSalariales.objects.get(pk=id)
                    o_Incremento.motivo_aumento = o_motivo
                    # o_Incremento.fecha_incremento = fecha_incremento
                    o_Incremento.incremento = incremento
                    o_Incremento.nuevo_salario = float(
                        o_Incremento.salario_anterior
                    ) + float(incremento)
                    o_Incremento.comentarios = comentarios
                    o_Incremento.user_mod = request.user
                    o_Incremento.date_mod = datetime.datetime.now()
                    o_Incremento.save()
                    o_empleado = Employee.objects.get(pk=o_Incremento.empleado.pk)
                    o_empleado.salary = float(o_Incremento.salario_anterior) + float(
                        incremento
                    )
                    o_empleado.salario_diario = (
                        float(o_Incremento.salario_anterior) + float(incremento)
                    ) / 30
                    o_empleado.save()
                    return JsonResponse(
                        {"error": False, "mensaje": "Se ha guardado el registro."}
                    )
                else:
                    return JsonResponse(
                        {"error": True, "mensaje": "El registro no existe."}
                    )
            else:
                return JsonResponse(
                    {"error": True, "mensaje": "El método no está permitido."}
                )
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
            return JsonResponse(data)
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": str(ex),
        }
        return JsonResponse(data)


def aumento_salario_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = IncrementosSalariales.objects.get(pk=reg_id)
                    empleado_id = oMd.empleado.pk
                    if oMd:
                        oMd.delete()
                        regs = IncrementosSalariales.objects.filter(empleado__pk=empleado_id).order_by("-fecha_incremento")[:1]
                        if regs.count() > 0:
                            incremento = regs[0]
                            incremento.salario_actual = True
                            incremento.save()
                            print(incremento.nuevo_salario)
                            regs = Employee.objects.filter(pk=empleado_id)
                            if regs.count() > 0:
                                empleado = Employee.objects.get(pk=empleado_id)
                                empleado.salary = incremento.nuevo_salario
                                if empleado.salaryUnits:
                                    tot_reg = SalaryUnit.objects.filter(
                                        pk=empleado.salaryUnits.pk
                                    ).count()
                                    if tot_reg > 0:
                                        o_salary_units = SalaryUnit.objects.get(
                                            pk=empleado.salaryUnits.pk
                                        )
                                        if int(o_salary_units.dias_salario) > 0:
                                            empleado.salario_diario = float(incremento.nuevo_salario) / 30
                                empleado.save()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }

    return JsonResponse(data)


def aumento_salario_ver_registro(request):
    error = False
    mensaje = ""
    titulo = ""
    dato = None
    id = 0
    if request.is_ajax():
        id = request.GET.get("id")
        if id == 0:
            error = True
            mensaje = "El registro no existe."
        else:
            tot_reg = IncrementosSalariales.objects.filter(pk=id).count()
            if tot_reg > 0:
                dato = IncrementosSalariales.objects.get(pk=id)
                dato = {
                    "pk": dato.pk,
                    "empleado": dato.empleado,
                    "fecha_incremento": dato.fecha_incremento,
                    "motivo_aumento": dato.motivo_aumento,
                    "salario_anterior": locale.format(
                        "%.2f", dato.salario_anterior, grouping=True
                    ),
                    "incremento": locale.format("%.2f", dato.incremento, grouping=True),
                    "nuevo_salario": locale.format(
                        "%.2f", dato.nuevo_salario, grouping=True
                    ),
                    "comentarios": dato.comentarios,
                }
                error = False
            else:
                error = True
                mensaje = "No existe el registro."
    else:
        error = True
        mensaje = "El método no está permitido."

    if error:
        titulo = "Error - Mensaje"
    else:
        titulo = "Ver registro"
    return render(
        request,
        "ajax/aumento-salario-modal.html",
        {"error": error, "mensaje": mensaje, "titulo": titulo, "dato": dato},
    )


def obtener_aumentos_salarios(request):
    print("Entro aqui")
    datos = []
    try:
        data = {}
        lista = []
        suc = Branch.objects.get(pk=request.session["sucursal"])
        lista = IncrementosSalariales.objects.filter(
            empresa_reg=suc.empresa, empleado__branch=suc, empleado__active=True
        )
        for item in lista:
            nombre = item.empleado.firstName
            if item.empleado.middleName:
                nombre += " " + item.empleado.middleName
            nombre += item.empleado.lastName
            fecha = datetime.datetime.strftime(item.fecha_incremento, "%d/%m/%Y")
            o_dato = {
                "id": item.pk,
                "codigo": item.empleado.extEmpNo,
                "identidad": item.empleado.govID,
                "empleado": nombre,
                "fecha": fecha,
                "es_salario_actual": item.salario_actual,
            }
            datos.append(o_dato)
        data = {"data": datos}
    except Exception as ex:
        print(ex)
        data = {"data": datos}
    return JsonResponse(data)


def obtener_aumentos_salarios2(request):
    lista = []
    data = {}
    datos = []
    try:
        suc = Branch.objects.get(pk=request.session["sucursal"])
        lista = IncrementosSalariales.objects.filter(empresa_reg=suc.empresa)
        for item in lista:
            nombre = item.empleado.firstName
            if item.empleado.middleName:
                nombre += " " + item.empleado.middleName
                nombre += item.empleado.lastName
            o_dato = {
                "id": item.pk,
                "codigo": item.empleado.extEmpNo,
                "empleado": nombre,
                "fecha": item.fecha_incremento,
                "es_salario_actual": item.salario_actual,
            }
            datos.append(o_dato)
            data = {"data": datos}
    except Exception as ex:
        data = {"error": True}
    return JsonResponse(data, safe=False)


def obtener_aumento_salario(request):
    try:
        data = {}
        if "id" in request.GET:
            reg_id = request.GET.get("id")
            reg_id = int(reg_id)
            o_datosalario = IncrementosSalariales.objects.get(pk=reg_id)
            nombre = o_datosalario.empleado.firstName
            if o_datosalario.empleado.middleName:
                nombre += " " + o_datosalario.empleado.middleName
            nombre += " " + o_datosalario.empleado.lastName
            data = {
                "pk": o_datosalario.pk,
                "empleado": o_datosalario.empleado.pk,
                "nombre_empleado": nombre,
                "motivo_aumento": o_datosalario.motivo_aumento.pk,
                "fecha_incremento": datetime.datetime.strftime(
                    o_datosalario.fecha_incremento, "%d/%m/%Y"
                ),
                "salario_anterior": formato_millar(o_datosalario.salario_anterior),
                "incremento": formato_millar(o_datosalario.incremento),
                "nuevo_salario": formato_millar(o_datosalario.nuevo_salario),
                "comentarios": o_datosalario.comentarios,
            }
            data = {"error": False, "data": data, "msg": "¡Exito!"}
        else:
            data = {"error": True, "msg": "No se esta pasando el parámetro"}
    except Exception as ex:
        data = {"error": True, "msg": str(ex)}
    return JsonResponse(data, status=200)


# ----------------- END AJAX --------------------


# endregion

# region Código para Deducción Individual


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_deduccionindividual", raise_exception=True)
def deduccion_individual_listado(request):
    listado = []
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_deduccionindividual"):
        listado = DeduccionIndividual.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_deduccionindividual"):
            listado = DeduccionIndividual.objects.filter(
                active=True, empresa_reg=suc.empresa
            )
    return render(request, "deduccion-individual-listado.html", {"listado": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_deduccionindividual", raise_exception=True)
def deduccion_individual_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    tipos_deducciones = TipoDeduccion.objects.filter(empresa_reg=suc.empresa)
    return render(
        request,
        "deduccion-individual-form.html",
        {"tipos_deducciones": tipos_deducciones},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_deduccionindividual", raise_exception=True)
def deduccion_individual_editar(request, id):
    dato = DeduccionIndividual.objects.get(pk=id)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    tipos_deducciones = TipoDeduccion.objects.filter(empresa_reg=suc.empresa)
    return render(
        request,
        "deduccion-individual-form.html",
        {"dato": dato, "editar": True, "tipos_deducciones": tipos_deducciones},
    )


# ---------------------AJAX-------------------------------


def deduccion_individual_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                deduccion = request.POST["deduccion"]
                tipo_deduccion = request.POST["tipo_deduccion"]
                controla_saldo = int(request.POST["controla_saldo"])
                activo = int(request.POST["activo"])

                if len(deduccion) == 0:
                    mensaje = "El campo 'Deducción Individual' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_deduccion) == 0:
                    mensaje = "El campo 'Tipo Deducción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(deduccion) > 50:
                    mensaje = "El campo 'Deducción' tiene como máximo 50 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if controla_saldo == 1:
                    controla_saldo = True
                else:
                    controla_saldo = False

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                o_tipodeduccion = TipoDeduccion.objects.get(pk=tipo_deduccion)

                oMd = DeduccionIndividual(
                    deduccion_i=deduccion,
                    tipo_deduccion=o_tipodeduccion,
                    control_saldo=controla_saldo,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def deduccion_individual_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                deduccion = request.POST["deduccion"]
                tipo_deduccion = request.POST["tipo_deduccion"]
                controla_saldo = int(request.POST["controla_saldo"])
                activo = int(request.POST["activo"])

                if len(deduccion) == 0:
                    mensaje = "El campo 'Deducción Individual' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_deduccion) == 0:
                    mensaje = "El campo 'Tipo Deducción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(deduccion) > 50:
                    mensaje = "El campo 'Deducción' tiene como máximo 50 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if controla_saldo == 1:
                    controla_saldo = True
                else:
                    controla_saldo = False

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                o_tipodeduccion = TipoDeduccion.objects.get(pk=tipo_deduccion)

                oMd = DeduccionIndividual.objects.get(pk=id)
                if oMd:
                    oMd.deduccion_i = deduccion
                    oMd.tipo_deduccion = o_tipodeduccion
                    oMd.control_saldo = controla_saldo
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def deduccion_individual_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = DeduccionIndividual.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------AJAX-------------------------------

# endregion

# region Código para Deducción Individual Detalle


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_deduccionindividualdetalle", raise_exception=True)
def deduccion_individual_detalle_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista = DeduccionIndividualDetalle.objects.filter(
        empresa_reg=suc.empresa, active=True
    ).order_by("-id")
    # if request.user.has_perm("worksheet.see_all_deduccionindividualdetalle"):
    #     lista = DeduccionIndividualDetalle.objects.filter(empresa_reg=suc.empresa)
    # else:
    #     lista = DeduccionIndividualDetalle.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(
        request, "deduccion-individual-detalle-listado.html", {"lista": lista}
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_ingresoindividualdetalle", raise_exception=True)
def deduccion_individual_detalle_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    deducciones = DeduccionIndividual.objects.filter(
        empresa_reg=suc.empresa, active=True
    )
    empleados = Employee.objects.filter(
        empresa_reg=suc.empresa, active=True, branch=suc
    )
    return render(
        request,
        "deduccion-individual-detalle-form.html",
        {"deducciones": deducciones, "empleados": empleados},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_ingresogeneraldetalle", raise_exception=True)
def deduccion_indidvidual_detalle_editar(request, id):

    tiene_detalle = False
    subdetalle = None
    dato = DeduccionIndividualDetalle.objects.get(pk=id)
    if DeduccionIndividualSubDetalle.objects.filter(deducciondetalle=dato).exists():
        tiene_detalle = True

        subdetalle = DeduccionIndividualSubDetalle.objects.get(deducciondetalle=dato)

    suc = Branch.objects.get(pk=request.session["sucursal"])
    deducciones = DeduccionIndividual.objects.filter(
        empresa_reg=suc.empresa, active=True
    )
    empleados = Employee.objects.filter(
        empresa_reg=suc.empresa, active=True, branch=suc
    )
    return render(
        request,
        "deduccion-individual-detalle-form.html",
        {
            "dato": dato,
            "deducciones": deducciones,
            "empleados": empleados,
            "editar": True,
            "detalle": tiene_detalle,
            "subdetalle": subdetalle,
        },
    )


# ----------------- END AJAX --------------------


def deduccion_individual_detalle_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                deduccion_id = request.POST["deduccion"]
                empleado_id = request.POST["empleado"]
                valor = request.POST["valor"]
                fecha_valida = request.POST["fecha"]
                activo = request.POST["activo"]
                descripcion = request.POST["descripcion"]
                monto = request.POST["monto"]

                if len(deduccion_id) == 0:
                    mensaje = "El campo 'Deducción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(empleado_id) == 0:
                    mensaje = "El campo 'Empleado' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) == 0:
                    mensaje = "El campo 'Valor' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(fecha_valida) == 0:
                    mensaje = "El campo 'Válido hasta' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(activo) == 0:
                    mensaje = "El campo 'Activo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                valor = valor.replace(",", "")

                if not validarEntero(deduccion_id):
                    mensaje = "El campo 'Deducción' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(empleado_id):
                    mensaje = "El campo'mpleado' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor):
                    mensaje = "El campo 'Valor' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(activo):
                    mensaje = "El campo 'Activo' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if deduccion_id == 0:
                    mensaje = "El re gistro del campo 'Deduccion' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if empleado_id == 0:
                    mensaje = "El registro del campo 'Empleado' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) > 18:
                    mensaje = "El campo 'Valor' tiene como máximo 18 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if float(valor) == 0:
                    mensaje = "El campo 'Valor' debe ser mayor a cero (0)."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) < 0 and int(valor) > 2:
                    mensaje = "El valor del campo 'Activo' no es válido."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                fecha_valida = datetime.datetime.strptime(fecha_valida, "%d/%m/%Y")
                fecha_valida = datetime.datetime.strftime(fecha_valida, "%Y-%m-%d")
                vdeduccion = DeduccionIndividual.objects.get(pk=deduccion_id)
                vempleado = Employee.objects.get(pk=empleado_id)
                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = DeduccionIndividualDetalle(
                    deduccion=vdeduccion,
                    empleado=vempleado,
                    valor=valor,
                    fecha_valida=fecha_valida,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()

                if not len(descripcion) == 0 or monto == 0:
                    o = DeduccionIndividualSubDetalle(
                        descripcion=descripcion,
                        deducciondetalle=oMd,
                        monto=monto,
                        user_reg=request.user,
                    )
                    o.save()

                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": str(ex),
        }
    return JsonResponse(data)


def deduccion_individual_detalle_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                deduccion_id = request.POST["deduccion"]
                empleado_id = request.POST["empleado"]
                valor = request.POST["valor"]
                fecha_valida = request.POST["fecha"]
                descripcion = request.POST["descripcion"]
                monto = request.POST["monto"]
                activo = request.POST["activo"]

                if len(deduccion_id) == 0:
                    mensaje = "El campo 'Deducción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(empleado_id) == 0:
                    mensaje = "El campo 'Empleado' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) == 0:
                    mensaje = "El campo 'Valor' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(fecha_valida) == 0:
                    mensaje = "El campo 'Válido hasta' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(activo) == 0:
                    mensaje = "El campo 'Activo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                valor = valor.replace(",", "")

                if not validarEntero(deduccion_id):
                    mensaje = "El campo 'Deducción' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(empleado_id):
                    mensaje = "El campo 'Empleado' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor):
                    mensaje = "El campo 'Valor' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(activo):
                    mensaje = "El campo 'Activo' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if deduccion_id == 0:
                    mensaje = "El registro del campo 'Deducción' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if empleado_id == 0:
                    mensaje = "El registro del campo 'Empleado' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) > 18:
                    mensaje = "El campo 'Valor' tiene como máximo 18 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if float(valor) == 0:
                    mensaje = "El campo 'Valor' debe ser mayor a cero (0)."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) < 0 and int(valor) > 2:
                    mensaje = "El valor del campo 'Activo' no es válido."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                fecha_valida = datetime.datetime.strptime(fecha_valida, "%d/%m/%Y")
                fecha_valida = datetime.datetime.strftime(fecha_valida, "%Y-%m-%d")

                vdeduccion = DeduccionIndividual.objects.get(pk=deduccion_id)
                vempleado = Employee.objects.get(pk=empleado_id)
                suc = Branch.objects.get(pk=request.session["sucursal"])
                oMd = DeduccionIndividualDetalle.objects.get(pk=id)
                if oMd:
                    oMd.deduccion = vdeduccion
                    oMd.empleado = vempleado
                    oMd.valor = valor
                    oMd.fecha_valida = fecha_valida
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}

                if DeduccionIndividualSubDetalle.objects.filter(
                    deducciondetalle=oMd
                ).exists():
                    subdetalle = DeduccionIndividualSubDetalle.objects.get(
                        deducciondetalle=oMd
                    )
                    if not len(descripcion) == 0 or monto == 0:
                        subdetalle.descripcion = descripcion
                        subdetalle.monto = monto
                        subdetalle.save()
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": str(ex),
        }
    return JsonResponse(data)


def deduccion_individual_detalle_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = DeduccionIndividualDetalle.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ----------------- END AJAX --------------------

# endregion

# region Código para Deducción Individual Planilla


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_deduccionindividualplanilla", raise_exception=True)
def deduccion_individual_planilla_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista = DeduccionIndividualPlanilla.objects.filter(sucursal_reg=suc, active=True)
    # if request.user.has_perm("worksheet.see_all_deduccionindividualdetalle"):
    #     lista = DeduccionIndividualPlanilla.objects.filter(empresa_reg=suc.empresa)
    # else:
    #     lista = DeduccionIndividualPlanilla.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(
        request, "deduccion-individual-planilla-listado.html", {"lista": lista}
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_deduccionindividualplanilla", raise_exception=True)
def deduccion_individual_planilla_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    deducciones = DeduccionIndividual.objects.filter(
        empresa_reg=suc.empresa, active=True
    )
    empleados = Employee.objects.filter(
        empresa_reg=suc.empresa, active=True, branch=suc
    )
    planillas = Planilla.objects.filter(sucursal_reg=suc, active=True)
    return render(
        request,
        "deduccion-individual-planilla-form.html",
        {"deducciones": deducciones, "empleados": empleados, "planillas": planillas},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_ingresogeneraldetalle", raise_exception=True)
def deduccion_indidvidual_planilla_editar(request, id):
    dato = DeduccionIndividualPlanilla.objects.get(pk=id)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    deducciones = DeduccionIndividual.objects.filter(
        empresa_reg=suc.empresa, active=True
    )
    empleados = Employee.objects.filter(
        empresa_reg=suc.empresa, active=True, branch=suc
    )
    planillas = Planilla.objects.filter(sucursal_reg=suc, active=True)
    return render(
        request,
        "deduccion-individual-planilla-form.html",
        {
            "dato": dato,
            "deducciones": deducciones,
            "empleados": empleados,
            "editar": True,
            "planillas": planillas,
        },
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_ingresogeneraldetalle", raise_exception=True)
def deduccion_individual_planilla_archivo(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    deducciones = DeduccionIndividual.objects.filter(
        empresa_reg=suc.empresa, active=True
    )
    planillas = Planilla.objects.filter(sucursal_reg=suc, active=True, cerrada=False)
    form = DeduccionArchivoForm()
    return render(
        request,
        "deduccion-individual-planilla-archivo.html",
        {"deducciones": deducciones, "planillas": planillas, "form": form},
    )


def deduccion_individual_planilla_archivo_guardar(request):
    datos = []
    lista_bulk = []
    try:
        if request.is_ajax():
            if request.method == "POST":
                deduccion_id = request.POST["deduccion"]
                planilla_id = request.POST["planilla"]
                if not DeduccionIndividual.objects.filter(pk=deduccion_id).exists():
                    data = {
                        "error": True,
                        "msj": 'El campo "Deducción" es obligatorio / Seleccione un valor válido para éste campo',
                    }
                    return JsonResponse(data)

                if not Planilla.objects.filter(pk=planilla_id).exists():
                    data = {
                        "error": True,
                        "msj": 'El campo "Planilla" es obligatorio / Seleccione un valor válido para éste campo',
                    }
                    return JsonResponse(data)

                form = DeduccionArchivoForm(request.POST, request.FILES)
                if form.is_valid():
                    suc = Branch.objects.get(pk=request.session["sucursal"])
                    bandera = False
                    planilla = Planilla.objects.get(pk=planilla_id)
                    deduccion = DeduccionIndividual.objects.get(pk=deduccion_id)
                    datosf = request.FILES["archivo"]
                    df = pandas.read_excel(
                        datosf, sheet_name="Deducciones", usecols=["Identidad", "Monto"]
                    )
                    datos = df.to_dict(orient="record")
                    identidad = ""
                    for item in datos:
                        identidad = item["Identidad"]
                        if Employee.objects.filter(
                            govID=identidad, active=True, branch=suc
                        ).exists():
                            print(identidad)
                            o_emplea = Employee.objects.get(
                                govID=identidad, active=True, branch=suc
                            )
                            if o_emplea.branch != suc:
                                data = {
                                    "error": True,
                                    "msj": "El empleado con identidad: "
                                    + identidad
                                    + ", no está asigando a la sucursal en sesión.",
                                }
                                return JsonResponse(data)
                            if DeduccionIndividualPlanilla.objects.filter(
                                planilla=planilla,
                                empleado=o_emplea,
                                deduccion=deduccion,
                            ).exists():
                                data = {
                                    "error": True,
                                    "msj": "El empleado con identidad: "
                                    + identidad
                                    + ", ya tiene aplicada la deducción seleccionada.",
                                }
                                return JsonResponse(data)
                        else:
                            bandera = True
                        if bandera:
                            break

                    if bandera:
                        data = {
                            "error": True,
                            "msj": "No existe empleado con Identidad: " + identidad,
                        }
                        return JsonResponse(data)

                    for empleado in datos:
                        o_empleado = Employee.objects.get(
                            govID=empleado["Identidad"], active=True, branch=suc
                        )
                        o_ded = DeduccionIndividualPlanilla(
                            planilla=planilla,
                            empleado=o_empleado,
                            deduccion=deduccion,
                            valor=empleado["Monto"],
                            empresa_reg=suc.empresa,
                            sucursal_reg=suc,
                            user_reg=request.user,
                            active=True,
                        )
                        lista_bulk.append(o_ded)
                    DeduccionIndividualPlanilla.objects.bulk_create(lista_bulk)
                    data = {
                        "error": False,
                        "msj": "Se han cargado " + str(len(datos)) + " registros",
                    }
                else:
                    data = {"error": True, "msj": "Los datos no están completos"}
            else:
                data = {"error": True, "msj": "Método no válido"}
        else:
            data = {"error": True, "msj": "Petición no asíncrona"}
    except Exception as ex:
        data = {"error": True, "msj": str(ex)}
    return JsonResponse(data)


# ----------------- END AJAX --------------------


def deduccion_individual_planilla_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                deduccion_id = request.POST["deduccion"]
                empleado_id = request.POST["empleado"]
                valor = request.POST["valor"]
                planilla_id = request.POST["planilla"]
                activo = request.POST["activo"]

                if len(deduccion_id) == 0:
                    mensaje = "El campo 'Deducción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(empleado_id) == 0:
                    mensaje = "El campo 'Empleado' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) == 0:
                    mensaje = "El campo 'Valor' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(planilla_id) == 0:
                    mensaje = "El campo 'Planilla' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(activo) == 0:
                    mensaje = "El campo 'Activo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                valor = valor.replace(",", "")

                if not validarEntero(deduccion_id):
                    mensaje = "El campo 'Deducción' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(empleado_id):
                    mensaje = "El campo 'Empleado' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(planilla_id):
                    mensaje = "El campo 'Planilla' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor):
                    mensaje = "El campo 'Valor' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(activo):
                    mensaje = "El campo 'Activo' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if deduccion_id == 0:
                    mensaje = "El registro del campo 'Deduccion' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if empleado_id == 0:
                    mensaje = "El registro del campo 'Empleado' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if planilla_id == 0:
                    mensaje = "El registro del campo 'Planilla' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) > 18:
                    mensaje = "El campo 'Valor' tiene como máximo 18 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if float(valor) == 0:
                    mensaje = "El campo 'Valor' debe ser mayor a cero (0)."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) < 0 and int(valor) > 2:
                    mensaje = "El valor del campo 'Activo' no es válido."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                vdeduccion = DeduccionIndividual.objects.get(pk=deduccion_id)
                vempleado = Employee.objects.get(pk=empleado_id)
                vplanilla = Planilla.objects.get(pk=planilla_id)
                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = DeduccionIndividualPlanilla(
                    deduccion=vdeduccion,
                    empleado=vempleado,
                    valor=valor,
                    planilla=vplanilla,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def deduccion_individual_planilla_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                deduccion_id = request.POST["deduccion"]
                empleado_id = request.POST["empleado"]
                valor = request.POST["valor"]
                planilla_id = request.POST["planilla"]
                activo = request.POST["activo"]

                if len(deduccion_id) == 0:
                    mensaje = "El campo 'Deducción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(empleado_id) == 0:
                    mensaje = "El campo 'Empleado' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) == 0:
                    mensaje = "El campo 'Valor' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(planilla_id) == 0:
                    mensaje = "El campo 'Planilla' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(activo) == 0:
                    mensaje = "El campo 'Activo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                valor = valor.replace(",", "")

                if not validarEntero(deduccion_id):
                    mensaje = "El campo 'Deducción' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(empleado_id):
                    mensaje = "El campo 'Empleado' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(planilla_id):
                    mensaje = "El campo 'Planilla' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor):
                    mensaje = "El campo 'Valor' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(activo):
                    mensaje = "El campo 'Activo' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if deduccion_id == 0:
                    mensaje = "El registro del campo 'Deducción' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if empleado_id == 0:
                    mensaje = "El registro del campo 'Empleado' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if planilla_id == 0:
                    mensaje = "El registro del campo 'Planilla' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) > 18:
                    mensaje = "El campo 'Valor' tiene como máximo 18 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if float(valor) == 0:
                    mensaje = "El campo 'Valor' debe ser mayor a cero (0)."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) < 0 and int(valor) > 2:
                    mensaje = "El valor del campo 'Activo' no es válido."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                vdeduccion = DeduccionIndividual.objects.get(pk=deduccion_id)
                vempleado = Employee.objects.get(pk=empleado_id)
                vplanilla = Planilla.objects.get(pk=planilla_id)
                suc = Branch.objects.get(pk=request.session["sucursal"])
                oMd = DeduccionIndividualPlanilla.objects.get(pk=id)
                if oMd:
                    oMd.deduccion = vdeduccion
                    oMd.empleado = vempleado
                    oMd.valor = valor
                    oMd.planilla = vplanilla
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def deduccion_individual_planilla_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = DeduccionIndividualPlanilla.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ----------------- END AJAX --------------------

# endregion

# region Código para Deducción General


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_deducciongeneral", raise_exception=True)
def deduccion_general_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    listado = DeduccionGeneral.objects.filter(active=True, empresa_reg=suc.empresa)
    # if request.user.has_perm("worksheet.see_all_deducciongeneral"):
    #     listado = DeduccionGeneral.objects.filter(empresa_reg=suc.empresa)
    # else:
    #     if request.user.has_perm("worksheet.see_deducciongeneral"):
    #         listado = DeduccionGeneral.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "deduccion-general-listado.html", {"listado": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_deducciongenearl", raise_exception=True)
def deduccion_general_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    tipos_deducciones = TipoDeduccion.objects.filter(empresa_reg=suc.empresa)
    return render(
        request, "deduccion-general-form.html", {"tipos_deducciones": tipos_deducciones}
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_deducciongeneral", raise_exception=True)
def deduccion_general_editar(request, id):
    dato = DeduccionGeneral.objects.get(pk=id)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    tipos_deducciones = TipoDeduccion.objects.filter(empresa_reg=suc.empresa)
    return render(
        request,
        "deduccion-general-form.html",
        {"dato": dato, "editar": True, "tipos_deducciones": tipos_deducciones},
    )


# ---------------------AJAX-------------------------------


def deduccion_general_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                deduccion = request.POST["deduccion"]
                tipo_deduccion = request.POST["tipo_deduccion"]
                activo = int(request.POST["activo"])

                if len(deduccion) == 0:
                    mensaje = "El campo 'Deducción General' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_deduccion) == 0:
                    mensaje = "El campo 'Tipo Deducción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(deduccion) > 50:
                    mensaje = (
                        "El campo 'Deducción General' tiene como máximo 50 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                o_tipodeduccion = TipoDeduccion.objects.get(pk=tipo_deduccion)

                oMd = DeduccionGeneral(
                    deduccion_g=deduccion,
                    tipo_deduccion=o_tipodeduccion,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def deduccion_general_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                deduccion = request.POST["deduccion"]
                tipo_deduccion = request.POST["tipo_deduccion"]
                activo = int(request.POST["activo"])

                if len(deduccion) == 0:
                    mensaje = "El campo 'Deducción General' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_deduccion) == 0:
                    mensaje = "El campo 'Tipo Deducción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(deduccion) > 50:
                    mensaje = (
                        "El campo 'Deducción General' tiene como máximo 50 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                o_tipodeduccion = TipoDeduccion.objects.get(pk=tipo_deduccion)

                oMd = DeduccionGeneral.objects.get(pk=id)
                if oMd:
                    oMd.deduccion_g = deduccion
                    oMd.tipo_deduccion = o_tipodeduccion
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def deduccion_general_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = DeduccionGeneral.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------AJAX-------------------------------

# endregion

# region Código para Deduccion General Detalle


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_deducciongeneraldetalle", raise_exception=True)
def deduccion_general_detalle_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    listado = DeduccionGeneralDetalle.objects.filter(active=True, sucursal_reg=suc)
    # if request.user.has_perm("worksheet.see_all_deducciongeneral"):
    #     listado = DeduccionGeneralDetalle.objects.filter(empresa_reg=suc.empresa)
    # else:
    #     if request.user.has_perm("worksheet.see_deducciongeneral"):
    #         listado = DeduccionGeneralDetalle.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(
        request, "deduccion-general-detalle-listado.html", {"listado": listado}
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_deducciongeneraldetalle", raise_exception=True)
def deduccion_general_detalle_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    deducciones = DeduccionGeneral.objects.filter(empresa_reg=suc.empresa, active=True)
    planillas = Planilla.objects.filter(sucursal_reg=suc, active=True)
    tipos_pagos = SalaryUnit.objects.filter(empresa_reg=suc.empresa, active=True)
    tipos_contratos = TipoContrato.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(
        request,
        "deduccion-general-detalle-form.html",
        {
            "deducciones": deducciones,
            "planillas": planillas,
            "tipos_pagos": tipos_pagos,
            "tipos_contratos": tipos_contratos,
        },
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_deducciongeneral", raise_exception=True)
def deduccion_general_detalle_editar(request, id):
    dato = DeduccionGeneralDetalle.objects.get(pk=id)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    deducciones = DeduccionGeneral.objects.filter(empresa_reg=suc.empresa, active=True)
    planillas = Planilla.objects.filter(sucursal_reg=suc, active=True)
    tipos_pagos = SalaryUnit.objects.filter(empresa_reg=suc.empresa, active=True)
    tipos_contratos = TipoContrato.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(
        request,
        "deduccion-general-detalle-form.html",
        {
            "dato": dato,
            "editar": True,
            "deducciones": deducciones,
            "planillas": planillas,
            "tipos_pagos": tipos_pagos,
            "tipos_contratos": tipos_contratos,
        },
    )


# ---------------------------AJAX-----------------------------


def deduccion_general_detalle_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                deduccion = request.POST["deduccion"]
                nomina = request.POST["nomina"]
                tipo_pago = request.POST["tipo_pago"]
                tipo_contrato = request.POST["tipo_contrato"]
                valor = request.POST["valor"]
                fecha_valida = request.POST["fecha"]
                activo = request.POST["activo"]

                if len(deduccion) == 0:
                    mensaje = "El campo 'Deducción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(nomina) == 0:
                    mensaje = "El campo 'Nómina' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_pago) == 0:
                    mensaje = "El campo 'Tipo de Pago' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_contrato) == 0:
                    mensaje = "El campo 'Tipo de Contrato' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) == 0:
                    mensaje = "El campo 'Valor' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(fecha_valida) == 0:
                    mensaje = "El campo 'Válido hasta' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(activo) == 0:
                    mensaje = "El campo 'Activo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                valor = valor.replace(",", "")

                if not validarEntero(deduccion):
                    mensaje = "El campo 'Deducción' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(nomina):
                    mensaje = "El campo 'Planilla' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(tipo_pago):
                    mensaje = "El campo 'Tipo de Pago' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(tipo_contrato):
                    mensaje = "El campo 'Tipo de Contrato' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor):
                    mensaje = "El campo 'Valor' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(activo):
                    mensaje = "El campo 'Activo' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if deduccion == 0:
                    mensaje = "El registro del campo 'Deducción' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if nomina == 0:
                    mensaje = "El registro del campo 'Nómina' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if tipo_pago == 0:
                    mensaje = "El registro del campo 'Tipo de Pago' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if tipo_contrato == 0:
                    mensaje = "El registro del campo 'Tipo de Contrato' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) > 18:
                    mensaje = (
                        "El campo 'Ingreso General' tiene como máximo 18 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if float(valor) == 0:
                    mensaje = "El campo 'Valor' debe ser mayor a cero (0)."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) < 0 and int(valor) > 2:
                    mensaje = "El valor del campo 'Activo' no es válido."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                vdeduccion = DeduccionGeneral.objects.get(pk=deduccion)
                vnomina = Planilla.objects.get(pk=nomina)
                vtipopago = SalaryUnit.objects.get(pk=tipo_pago)
                vtipocontrato = TipoContrato.objects.get(pk=tipo_contrato)
                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = DeduccionGeneralDetalle(
                    deduccion=vdeduccion,
                    nomina=vnomina,
                    tipo_pago=vtipopago,
                    tipo_contrato=vtipocontrato,
                    valor=valor,
                    fecha_valido=fecha_valida,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def deduccion_general_detalle_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = request.POST["id"]
                deduccion = request.POST["deduccion"]
                nomina = request.POST["nomina"]
                tipo_pago = request.POST["tipo_pago"]
                tipo_contrato = request.POST["tipo_contrato"]
                valor = request.POST["valor"]
                fecha_valida = request.POST["fecha"]
                activo = request.POST["activo"]

                if len(deduccion) == 0:
                    mensaje = "El campo 'Deducción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(nomina) == 0:
                    mensaje = "El campo 'Nómina' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_pago) == 0:
                    mensaje = "El campo 'Tipo de Pago' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_contrato) == 0:
                    mensaje = "El campo 'Tipo de Contrato' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) == 0:
                    mensaje = "El campo 'Valor' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(fecha_valida) == 0:
                    mensaje = "El campo 'Válido hasta' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(activo) == 0:
                    mensaje = "El campo 'Activo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                valor = valor.replace(",", "")

                if not validarEntero(deduccion):
                    mensaje = "El campo 'Deducción' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(nomina):
                    mensaje = "El campo 'Planilla' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(tipo_pago):
                    mensaje = "El campo 'Tipo de Pago' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(tipo_contrato):
                    mensaje = "El campo 'Tipo de Contrato' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor):
                    mensaje = "El campo 'Valor' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(activo):
                    mensaje = "El campo 'Activo' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if deduccion == 0:
                    mensaje = "El registro del campo 'Deducción' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if nomina == 0:
                    mensaje = "El registro del campo 'Nómina' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if tipo_pago == 0:
                    mensaje = "El registro del campo 'Tipo de Pago' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if tipo_contrato == 0:
                    mensaje = "El registro del campo 'Tipo de Contrato' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) > 18:
                    mensaje = "El campo 'Valor' tiene como máximo 18 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if float(valor) == 0:
                    mensaje = "El campo 'Valor' debe ser mayor a cero (0)."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) < 0 and int(valor) > 2:
                    mensaje = "El valor del campo 'Activo' no es válido."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                vdeduccion = DeduccionGeneral.objects.get(pk=deduccion)
                vnomina = Planilla.objects.get(pk=nomina)
                vtipopago = SalaryUnit.objects.get(pk=tipo_pago)
                vtipocontrato = TipoContrato.objects.get(pk=tipo_contrato)
                suc = Branch.objects.get(pk=request.session["sucursal"])
                oMd = DeduccionGeneralDetalle.objects.get(pk=id)
                if oMd:
                    oMd.deduccion = vdeduccion
                    oMd.nomina = vnomina
                    oMd.tipo_pago = vtipopago
                    oMd.tipo_contrato = vtipocontrato
                    oMd.valor = valor
                    oMd.fecha_valido = fecha_valida
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def deduccion_general_detalle_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = DeduccionGeneralDetalle.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------------AJAX-----------------------------

# endregion

# region Código para Empleado

# ---------------------------AJAX-----------------------------


def obtener_dias_salario(request):
    try:
        if request.is_ajax():
            Id = request.GET.get("id")
            tot_reg = SalaryUnit.objects.filter(pk=Id)
            if tot_reg.count() > 0:
                tipo_salario = SalaryUnit.objects.get(pk=Id)
                return JsonResponse(
                    {
                        "error": False,
                        "mensaje": "Respuesta exitosa",
                        "dias_salario": tipo_salario.dias_salario,
                    }
                )
            else:
                return JsonResponse(
                    {"error": True, "mensaje": "El tipo de salario no existe."}
                )
        else:
            return JsonResponse({"error": True, "mensaje": "El método no es asíncrono"})
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": ex.message,
        }
        return JsonResponse(data)


def obtener_deducciones(request):
    deducciones = []
    tipos_deducciones = []
    data = {"data": None}
    if request.is_ajax():
        suc = Branch.objects.get(pk=request.session["sucursal"])
        empleado_id = request.GET.get("empleado_id")
        deducciones = EmpleadoDeducciones.objects.filter(
            empleado__id=empleado_id, active=True
        )
        tipos_deducciones = TipoDeduccion.objects.filter(
            empresa_reg=suc.empresa, active=True
        )

    return render(request, "ajax/deducciones_empleado.html", {"deducciones": deducciones, "tipos_deducciones": tipos_deducciones})


def obtener_deduccion_empleado(request):
    data = {}
    if request.is_ajax():
        suc = Branch.objects.get(pk=request.session["sucursal"])
        registro_id = request.GET.get("id")
        deduccion = EmpleadoDeducciones.objects.get(pk=registro_id)
        data = {
            "pk": deduccion.pk,
            "deduccion": deduccion.deduccion,
            "periodo": deduccion.periodo,
            "deduccion_parcial": deduccion.deduccion_parcial,
            "activo": deduccion.active,
            "error": False,
        }
    return JsonResponse(data)


def eliminar_empleado_deduccion(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = EmpleadoDeducciones.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# --------------------------END AJAX -------------------------

# endregion

# region Código para Deduccion Empleado

# ------------------------->>> AJAX <<<--------------------------


def guardar_deduccion_empleado(request):
    try:
        data = {}
        if request.is_ajax():
            if request.method == "POST":

                pdeduccion = request.POST["deduccion"]
                ptipoperiodo = request.POST["tipo_periodo"]
                pperiodo = request.POST["periodo"]
                pactivo = request.POST["activo"]
                pempleado = request.POST["empleado"]

                if pdeduccion == "0":
                    data = {
                        "error": True,
                        "mensaje": 'El campo "Deduccion" es obligatorio',
                    }
                    return JsonResponse(data)

                if int(ptipoperiodo) == 0:
                    print(int(ptipoperiodo))
                    pperiodo = 1

                if int(pperiodo) == 0:
                    data = {
                        "error": True,
                        "mensaje": 'El campo "Periodo" es obligatorio',
                    }
                    return JsonResponse(data)
                if len(pempleado) == 0:
                    data = {
                        "error": True,
                        "mensaje": "El campo empleado es obligatorio",
                    }
                    return JsonResponse(data)
                elif pempleado == 0:
                    data = {
                        "error": True,
                        "mensaje": "No se pasó un valor válido para empleado",
                    }
                    return JsonResponse(data)
                o_empleado = Employee.objects.get(pk=pempleado)
                tot_reg = EmpleadoDeducciones.objects.filter(
                    empleado=o_empleado, deduccion=pdeduccion
                ).count()
                if tot_reg > 0:
                    tot_reg = EmpleadoDeducciones.objects.filter(
                        empleado=o_empleado, deduccion=pdeduccion, active=False
                    ).count()
                    if tot_reg > 0:
                        data = {
                            "error": True,
                            "mensaje": "La deducción seleccionada ya está asignada al empleado, el registro puede estar inactivo",
                        }
                    else:
                        data = {
                            "error": True,
                            "mensaje": "La deducción seleccionada ya está asignada al empleado",
                        }
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])
                o_empDed = EmpleadoDeducciones(
                    empleado=o_empleado,
                    deduccion=pdeduccion,
                    periodo=pperiodo,
                    deduccion_parcial=ptipoperiodo,
                    empresa_reg=suc.empresa,
                    user_reg=request.user,
                    active=True,
                )
                o_empDed.save()
                data = {"error": False, "mensaje": "El registro se ha creado"}
                return JsonResponse(data)
            else:
                data = {"error": True, "mensaje": "El método no es permitido"}
        else:
            data = {"error": True, "mensaje": "La petición no es asíncrona"}
        return JsonResponse(data)
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": ex.message,
        }
        return JsonResponse(data)


def actualizar_deduccion_empleado(request):
    print("Entro aqui")
    try:
        
        data = {}
        if request.is_ajax():
            if request.method == "POST":
                pdeduccion = request.POST["deduccion"]
                ptipoperiodo = request.POST["tipo_periodo"]
                pperiodo = request.POST["periodo"]
                pactivo = request.POST["activo"]
                pempleado = request.POST["empleado"]
                id = request.POST["id"]

                if pdeduccion == "0":
                    data = {
                        "error": True,
                        "mensaje": 'El campo "Deduccion" es obligatorio',
                    }
                    return JsonResponse(data)

                if int(ptipoperiodo) == 0:
                    print(int(ptipoperiodo))
                    pperiodo = 1

                if int(pperiodo) == 0:
                    data = {
                        "error": True,
                        "mensaje": 'El campo "Periodo" es obligatorio',
                    }
                    return JsonResponse(data)
                if len(pempleado) == 0:
                    data = {
                        "error": True,
                        "mensaje": "El campo empleado es obligatorio",
                    }
                    return JsonResponse(data)
                elif pempleado == 0:
                    data = {
                        "error": True,
                        "mensaje": "No se pasó un valor válido para empleado",
                    }
                    return JsonResponse(data)

                tot_reg = Employee.objects.filter(pk=pempleado).count()
                if tot_reg > 0:
                    o_empleado = Employee.objects.get(pk=pempleado)
                    tot_reg = EmpleadoDeducciones.objects.filter(pk=id).count()
                    if tot_reg > 0:

                        o_empDed = EmpleadoDeducciones.objects.get(pk=id)
                        tot_reg = (
                            EmpleadoDeducciones.objects.filter(
                                empleado=o_empleado, deduccion=pdeduccion
                            )
                            .exclude(pk=id)
                            .count()
                        )
                        if tot_reg > 0:
                            data = {
                                "error": True,
                                "mensaje": "No se puede actualizar, la deducción tiene otro registro de asignación para el empleado",
                            }
                            return JsonResponse(data)
                        else:
                            o_empDed.deduccion = pdeduccion
                            o_empDed.periodo = pperiodo
                            o_empDed.deduccion_parcial = ptipoperiodo
                            if pactivo == "true":
                                o_empDed.active = True
                            else:
                                o_empDed.active = False
                            o_empDed.save()
                            data = {
                                "error": False,
                                "mensaje": "Se ha actualizado el registro",
                            }
                            return JsonResponse(data)
                    else:
                        data = {
                            "error": True,
                            "mensaje": "El registro de deducción a empleado no existe",
                        }
                        return JsonResponse(data)
                else:
                    data = {"error": True, "mensaje": "El empleado no existe"}
                    return JsonResponse(data)
            else:
                data = {"error": True, "mensaje": "El método no está permitido"}
                return JsonResponse(data)
        else:
            data = {"error": True, "mensaje": "La petición no es asíncrona"}
            return JsonResponse(data)
    except Exception as ex:
        print(ex)
        data = {"error": True, "mensaje": "error"}
        return JsonResponse(data)


# ------------------------->>> AJAX <<<--------------------------

# endregion

# region Código para Horas Extras


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_horaextra", raise_exception=True)
def horaextra_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_horaextra"):
        lista = HoraExtra.objects.filter(empresa_reg=suc.empresa)
    else:
        lista = HoraExtra.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(request, "horasextras-listado.html", {"lista": lista})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_horaextra", raise_exception=True)
def horaextra_form(request):
    return render(request, "horaextra-form.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_horaextra", raise_exception=True)
def horaextra_editar(request, id):
    idreg = 0
    idreg = int(id)
    dato = HoraExtra.objects.get(pk=idreg)
    return render(request, "horaextra-form.html", {"dato": dato, "editar": True})


# ---------------------AJAX-------------------------------


def horaextra_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                jornada = request.POST["jornada"]
                horaini = request.POST["horaini"]
                horafin = request.POST["horafin"]
                horaDiarias = request.POST["horasDiarias"]
                horaSemanas = request.POST["horasSemana"]
                noexede = request.POST["noexede"]
                horaextra = request.POST["horaextra"]
                activo = int(request.POST["activo"])

                if len(jornada) == 0:
                    mensaje = "El campo 'Jornada' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(horaini) == 0:
                    mensaje = "El campo 'Hora Inicial' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(horafin) == 0:
                    mensaje = "El campo 'Hora Fin' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(horaDiarias) == 0:
                    mensaje = "El campo 'Horas Diarias' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(horaSemanas) == 0:
                    mensaje = "El campo 'Hora Semana' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(noexede) == 0:
                    mensaje = "El campo 'No Exede Nocturno' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(horaextra) == 0:
                    mensaje = "El campo 'Hora Extra' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                horaextra = horaextra.replace("%", "")

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = HoraExtra(
                    jornada=jornada,
                    horaini=horaini,
                    horafin=horafin,
                    horasDiarias=horaDiarias,
                    horasSemana=horaSemanas,
                    noExedeNocturno=noexede,
                    horaExtra=horaextra,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def horaextra_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                jornada = request.POST["jornada"]
                horaini = request.POST["horaini"]
                horafin = request.POST["horafin"]
                horaDiarias = request.POST["horasDiarias"]
                horaSemanas = request.POST["horasSemana"]
                noexede = request.POST["noexede"]
                horaextra = request.POST["horaextra"]
                activo = int(request.POST["activo"])

                if len(jornada) == 0:
                    mensaje = "El campo 'Jornada' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(horaini) == 0:
                    mensaje = "El campo 'Hora Inicial' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(horafin) == 0:
                    mensaje = "El campo 'Hora Fin' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(horaDiarias) == 0:
                    mensaje = "El campo 'Horas Diarias' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(horaSemanas) == 0:
                    mensaje = "El campo 'Hora Semana' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(noexede) == 0:
                    mensaje = "El campo 'No Exede Nocturno' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(horaextra) == 0:
                    mensaje = "El campo 'Hora Extra' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                horaextra = horaextra.replace("%", "")

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = HoraExtra.objects.get(pk=id)
                if oMd:
                    oMd.jornada = jornada
                    oMd.horaini = horaini
                    oMd.horafin = horafin
                    oMd.horasDiarias = horaDiarias
                    oMd.horasSemana = horaSemanas
                    oMd.noExedeNocturno = noexede
                    oMd.horaExtra = horaextra
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def horaextra_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = HoraExtra.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------AJAX-------------------------------

# endregion

# region Código para Impuesto sobre Renta


@login_required(login_url="/form/iniciar-sesion/")
def isr_encabezado(request):
    datos = []
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista_isr = EncabezadoImpuestoSobreRenta.objects.filter(empresa_reg=suc.empresa)
    print(lista_isr)
    for item in lista_isr:
        data = {
            "pk": item.pk,
            "codigo": item.codigo,
            "fecha_vigencia": item.fecha_vigencia,
            "descripcion": item.descripcion,
            "valor": formato_millar(item.valor),
            "descripcion1": item.descripcion1,
            "valor1": formato_millar(item.valor1),
            "descripcion2": item.descripcion2,
            "valor2": formato_millar(item.valor2),
        }
        datos.append(data)
    return render(request, "isr-encabezado-listado.html", {"lista": datos})


@login_required(login_url="/form/iniciar-sesion/")
def isr_encabezado_form(request):
    return render(request, "isr-encabezado-form.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_impuestosobrerenta", raise_exception=True)
def impuestosobrerenta_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_impuestosbrerenta"):
        lista = ImpuestoSobreRenta.objects.filter(empresa_reg=suc.empresa)
    else:
        lista = ImpuestoSobreRenta.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(request, "isr-listado.html", {"lista": lista})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_impuestosobrerenta", raise_exception=True)
def impuestosobrerenta_form(request):
    return render(request, "isr-form.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_ingresogeneral", raise_exception=True)
def impuestosobrerenta_editar(request, id):
    dato = ImpuestoSobreRenta.objects.get(pk=id)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    return render(request, "isr-form.html", {"dato": dato, "editar": True})


# ---------------------AJAX-------------------------------


def isr_encabezado_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                suc = Branch.objects.get(pk=request.session["sucursal"])
                codigo = request.POST["codigo"]
                fecha = request.POST["fecha"]
                deducible = request.POST["deducible"]
                valor = request.POST["valor"]
                deducible1 = request.POST["deducible1"]
                valor1 = request.POST["valor1"]
                deducible2 = request.POST["deducible2"]
                valor2 = request.POST["valor2"]

                if codigo:
                    if len(codigo) == 0:
                        data = {
                            "error": True,
                            "mensaje": 'El campo "Código" es obligatorio',
                        }
                        return JsonResponse(data)
                else:
                    data = {
                        "error": True,
                        "mensaje": 'El campo "Código" es obligatorio',
                    }
                    return JsonResponse(data)

                if fecha:
                    if len(fecha) == 0:
                        data = {
                            "error": True,
                            "mensaje": 'El campo "Fecha" es obligatorio',
                        }
                        return JsonResponse(data)
                else:
                    data = {"error": True, "mensaje": 'El campo "Fecha" es obligatorio'}
                    return JsonResponse(data)

                if valor:
                    valor = valor.replace(",", "")
                else:
                    valor = None
                    # mensaje = "El campo 'Valor' es de tipo decimal."
                    # data = {'error': True, 'mensaje': mensaje}
                    # return JsonResponse(data)

                if valor1:
                    valor1 = valor1.replace(",", "")
                else:
                    valor1 = None
                    # mensaje = "El campo 'Valor' es de tipo decimal."
                    # data = {'error': True, 'mensaje': mensaje}
                    # return JsonResponse(data)

                if valor2:
                    valor2 = valor2.replace(",", "")
                else:
                    valor2 = None
                    # mensaje = "El campo 'Porcentaje' es de tipo decimal."
                    # data = {'error': True, 'mensaje': mensaje}
                    # return JsonResponse(data)

                o_encabezado_isr = EncabezadoImpuestoSobreRenta(
                    codigo=codigo,
                    fecha_vigencia=fecha,
                    descripcion=deducible,
                    valor=valor,
                    descripcion1=deducible1,
                    valor1=valor1,
                    descripcion2=deducible2,
                    valor2=valor2,
                    empresa_reg=suc.empresa,
                    user_reg=request.user,
                    active=True,
                )
                o_encabezado_isr.save()
                data = {
                    "error": False,
                    "mensaje": "Se ha creado el registro",
                    "pk": o_encabezado_isr.pk,
                }
                return JsonResponse(data)
            else:
                data = {"error": True, "mensaje": "El método no es permitido."}
                return JsonResponse(data)
        else:
            data = {"error": True, "mensaje": "La petición no es asíncrona"}
            return JsonResponse(data)
    except Exception as ex:
        print(ex)
        data = {"error": True, "mensaje": "Error"}
        return JsonResponse(data)


def impuestosobrerenta_obtener(request):
    dato = None
    dato2 = None
    dato3 = None
    datos = []
    detalles = []
    # print(request)
    if request.is_ajax():
        registro_id = request.GET.get("Id")
        # datos = []
        # suc = Branch.objects.get(pk=request.session["sucursal"])
        # lista_isr = EncabezadoImpuestoSobreRenta.objects.filter(empresa_reg=suc.empresa)
        lista_isr = EncabezadoImpuestoSobreRenta.objects.filter(pk=registro_id)
        if lista_isr.count() > 0:
            dato = EncabezadoImpuestoSobreRenta.objects.get(pk=registro_id)
            dato2 = {
                "pk": dato.pk,
                "fecha_vigencia": dato.fecha_vigencia,
                "codigo": dato.codigo,
                "descripcion": dato.descripcion,
                "valor": formato_millar(dato.valor),
                "descripcion1": dato.descripcion1,
                "valor1": formato_millar(dato.valor1),
                "descripcion2": dato.descripcion2,
                "valor2": formato_millar(dato.valor2),
                "active": dato.active,
            }
            detalles = ImpuestoSobreRenta.objects.filter(encabezado=dato)

            for item in detalles:
                dato3 = {
                    "pk": item.pk,
                    "desde": formato_millar(item.desde),
                    "hasta": formato_millar(item.hasta),
                    "porcentaje": formato_millar(item.porcentaje),
                }
                datos.append(dato3)
    return render(
        request, "ajax/isr_encabezado.html", {"dato": dato2, "detalles": datos}
    )


def impuestosobrerenta_guardar(request):
    tot_reg = 0
    registro = {}
    try:
        if request.is_ajax():
            if request.method == "POST":

                desde = request.POST["desde"]
                hasta = request.POST["hasta"]
                encabezado = request.POST["isr_enc"]
                porcentaje = request.POST["porcentaje"]

                if len(desde) == 0:
                    mensaje = "El campo 'Desde' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(hasta) == 0:
                    mensaje = "El campo 'Hasta' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(porcentaje) == 0:
                    mensaje = "El campo 'Porcentaje' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(encabezado) == 0:
                    mensaje = "Se requiere seleccionar un valor para de registro 'Impuesto Sobre Venta'."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                desde = desde.replace(",", "")
                hasta = hasta.replace(",", "")
                porcentaje = porcentaje.replace(",", "")

                if not validarDecimal(desde):
                    mensaje = "El campo 'Desde' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(hasta):
                    mensaje = "El campo 'Desde' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(porcentaje):
                    mensaje = "El campo 'Porcentaje' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                # if activo == 1:
                #     activo = True
                # else:
                #     activo = False
                tot_reg = EncabezadoImpuestoSobreRenta.objects.filter().count()
                if tot_reg == 0:
                    mensaje = "El campo 'Porcentaje' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                enc = EncabezadoImpuestoSobreRenta.objects.get(pk=encabezado)
                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = ImpuestoSobreRenta(
                    desde=desde,
                    hasta=hasta,
                    porcentaje=porcentaje,
                    porcentaje_label=str(porcentaje) + "%",
                    encabezado=enc,
                    empresa_reg=suc.empresa,
                    active=True,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    "pk": oMd.pk,
                    "desde": oMd.desde,
                    "hasta": oMd.hasta,
                    "porcentaje": oMd.porcentaje,
                }
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False, "dato": registro}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def impuestosobrerenta_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desde = request.POST["desde"]
                hasta = request.POST["hasta"]
                porcentaje = request.POST["porcentaje"]
                activo = int(request.POST["activo"])

                if len(desde) == 0:
                    mensaje = "El campo 'Desde' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(hasta) == 0:
                    mensaje = "El campo 'Hasta' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(porcentaje) == 0:
                    mensaje = "El campo 'Porcentaje' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                # desde = desde.replace(".", "")
                # desde = desde.replace(",", ".")
                # hasta = hasta.replace(".", "")
                # hasta = hasta.replace(",", ".")
                # porcentaje = porcentaje.replace(".", "")
                # porcentaje = porcentaje.replace(",", ".")

                if not validarDecimal(desde):
                    mensaje = "El campo 'Desde' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(hasta):
                    mensaje = "El campo 'Desde' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(porcentaje):
                    mensaje = "El campo 'Porcentaje' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = ImpuestoSobreRenta.objects.get(pk=id)
                if oMd:
                    oMd.desde = float(desde)
                    oMd.hasta = float(hasta)
                    oMd.porcentaje = float(porcentaje)
                    oMd.porcentaje_label = str(porcentaje) + "%"
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": str(ex),
        }
    return JsonResponse(data)


def impuestosobrerenta_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = ImpuestoSobreRenta.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------AJAX-------------------------------

# endregion

# region Código para Ingreso General


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_ingresogeneral", raise_exception=True)
def ingreso_general_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_ingresogeneral"):
        lista = IngresoGeneral.objects.filter(empresa_reg=suc.empresa)
    else:
        lista = IngresoGeneral.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(request, "ingreso-general-listado.html", {"lista": lista})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_ingresogeneral", raise_exception=True)
def ingreso_general_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    tipos_ingresos = TipoIngreso.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(
        request, "ingreso-general-form.html", {"tipos_ingresos": tipos_ingresos}
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_ingresogeneral", raise_exception=True)
def ingreso_general_editar(request, id):
    dato = IngresoGeneral.objects.get(pk=id)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    tipos_ingresos = TipoIngreso.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(
        request,
        "ingreso-general-form.html",
        {"dato": dato, "tipos_ingresos": tipos_ingresos, "editar": True},
    )


# ---------------------AJAX-------------------------------


def ingreso_general_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                ingreso_g = request.POST["ingreso_g"]
                tipo_ingreso = request.POST["tipo_ingreso"]
                activo = int(request.POST["activo"])
                gravable = int(request.POST["gravable"])

                if len(ingreso_g) == 0:
                    mensaje = "El campo 'Ingreso General' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_ingreso) == 0:
                    mensaje = "El campo 'Tipo Ingreso' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if tipo_ingreso == 0:
                    mensaje = "El registro no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(ingreso_g) > 50:
                    mensaje = (
                        "El campo 'Ingreso General' tiene como máximo 50 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if gravable == 1:
                    gravable = True
                else:
                    gravable = False

                o_tipoingreso = TipoIngreso.objects.get(pk=tipo_ingreso)

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = IngresoGeneral(
                    ingreso_g=ingreso_g,
                    tipo_ingreso=o_tipoingreso,
                    gravable=gravable,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def ingreso_general_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                ingreso_g = request.POST["ingreso_g"]
                tipo_ingreso = request.POST["tipo_ingreso"]
                activo = int(request.POST["activo"])
                gravable = int(request.POST["gravable"])

                if len(ingreso_g) == 0:
                    mensaje = "El campo 'Ingreso General' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_ingreso) == 0:
                    mensaje = "El campo 'Tipo Ingreso' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if tipo_ingreso == 0:
                    mensaje = "El registro no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(ingreso_g) > 50:
                    mensaje = (
                        "El campo 'Ingreso General' tiene como máximo 50 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if gravable == 1:
                    gravable = True
                else:
                    gravable = False

                o_tipoingreso = TipoIngreso.objects.get(pk=tipo_ingreso)
                oMd = IngresoGeneral.objects.get(pk=id)
                if oMd:
                    oMd.ingreso_g = ingreso_g
                    oMd.tipo_ingreso = o_tipoingreso
                    oMd.gravable = gravable
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def ingreso_general_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = IngresoGeneral.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------AJAX-------------------------------

# endregion

# region Código para Ingreso General Detalle


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_ingresogeneraldetalle", raise_exception=True)
def ingreso_general_detalle_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista = IngresoGeneralDetalle.objects.filter(sucursal_reg=suc, active=True)
    # if request.user.has_perm("worksheet.see_all_ingresogeneral"):
    #     lista = IngresoGeneralDetalle.objects.filter(empresa_reg=suc.empresa)
    # else:
    #     lista = IngresoGeneralDetalle.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(request, "ingreso-general-detalle-listado.html", {"lista": lista})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_ingresogeneraldetalle", raise_exception=True)
def ingreso_general_detalle_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    ingresos_generales = IngresoGeneral.objects.filter(
        empresa_reg=suc.empresa, active=True
    )
    planillas = Planilla.objects.filter(sucursal_reg=suc, active=True)
    tipos_pagos = SalaryUnit.objects.filter(empresa_reg=suc.empresa, active=True)
    tipos_contratos = TipoContrato.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(
        request,
        "ingreso-general-detalle-form.html",
        {
            "ingresos_generales": ingresos_generales,
            "planillas": planillas,
            "tipos_pagos": tipos_pagos,
            "tipos_contratos": tipos_contratos,
        },
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_ingresogeneraldetalle", raise_exception=True)
def ingreso_general_detalle_editar(request, id):
    dato = IngresoGeneralDetalle.objects.get(pk=id)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    ingresos_generales = IngresoGeneral.objects.filter(
        empresa_reg=suc.empresa, active=True
    )
    planillas = Planilla.objects.filter(sucursal_reg=suc, active=True)
    tipos_pagos = SalaryUnit.objects.filter(empresa_reg=suc.empresa, active=True)
    tipos_contratos = TipoContrato.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(
        request,
        "ingreso-general-detalle-form.html",
        {
            "dato": dato,
            "ingresos_generales": ingresos_generales,
            "planillas": planillas,
            "tipos_pagos": tipos_pagos,
            "tipos_contratos": tipos_contratos,
            "editar": True,
        },
    )


# ---------------------AJAX-------------------------------


def ingreso_general_detalle_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                ingreso = request.POST["ingreso"]
                nomina = request.POST["nomina"]
                tipo_pago = request.POST["tipo_pago"]
                tipo_contrato = request.POST["tipo_contrato"]
                valor = request.POST["valor"]
                fecha_valida = request.POST["fecha"]
                activo = request.POST["activo"]

                if len(ingreso) == 0:
                    mensaje = "El campo 'Ingreso' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(nomina) == 0:
                    mensaje = "El campo 'Nómina' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_pago) == 0:
                    mensaje = "El campo 'Tipo de Pago' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_contrato) == 0:
                    mensaje = "El campo 'Tipo de Contrato' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) == 0:
                    mensaje = "El campo 'Valor' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(fecha_valida) == 0:
                    mensaje = "El campo 'Válido hasta' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(activo) == 0:
                    mensaje = "El campo 'Activo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                fecha_valida = datetime.datetime.strptime(fecha_valida, "%d/%m/%Y")
                fecha_valida = datetime.datetime.strftime(fecha_valida, "%Y-%m-%d")

                valor = valor.replace(",", "")

                if not validarEntero(ingreso):
                    mensaje = "El campo 'Ingreso' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(nomina):
                    mensaje = "El campo 'Planilla' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(tipo_pago):
                    mensaje = "El campo 'Tipo de Pago' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(tipo_contrato):
                    mensaje = "El campo 'Tipo de Contrato' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor):
                    mensaje = "El campo 'Valor' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(activo):
                    mensaje = "El campo 'Activo' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if ingreso == 0:
                    mensaje = "El registro del campo 'Ingreso' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if nomina == 0:
                    mensaje = "El registro del campo 'Nómina' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if tipo_pago == 0:
                    mensaje = "El registro del campo 'Tipo de Pago' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if tipo_contrato == 0:
                    mensaje = "El registro del campo 'Tipo de Contrato' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) > 18:
                    mensaje = (
                        "El campo 'Ingreso General' tiene como máximo 18 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if float(valor) == 0:
                    mensaje = "El campo 'Valor' debe ser mayor a cero (0)."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) < 0 and int(valor) > 2:
                    mensaje = "El valor del campo 'Activo' no es válido."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) == 1:

                    activo = True
                else:
                    activo = False

                vingreso = IngresoGeneral.objects.get(pk=ingreso)
                vnomina = Planilla.objects.get(pk=nomina)
                vtipopago = SalaryUnit.objects.get(pk=tipo_pago)
                vtipocontrato = TipoContrato.objects.get(pk=tipo_contrato)
                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = IngresoGeneralDetalle(
                    ingreso=vingreso,
                    nomina=vnomina,
                    tipo_pago=vtipopago,
                    tipo_contrato=vtipocontrato,
                    valor=valor,
                    fecha_valida=fecha_valida,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def ingreso_general_detalle_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                ingreso = request.POST["ingreso"]
                nomina = request.POST["nomina"]
                tipo_pago = request.POST["tipo_pago"]
                tipo_contrato = request.POST["tipo_contrato"]
                valor = request.POST["valor"]
                fecha_valida = request.POST["fecha"]
                activo = request.POST["activo"]

                if len(ingreso) == 0:
                    mensaje = "El campo 'Ingreso' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(nomina) == 0:
                    mensaje = "El campo 'Nómina' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_pago) == 0:
                    mensaje = "El campo 'Tipo de Pago' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_contrato) == 0:
                    mensaje = "El campo 'Tipo de Contrato' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) == 0:
                    mensaje = "El campo 'Valor' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(fecha_valida) == 0:
                    mensaje = "El campo 'Válido hasta' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(activo) == 0:
                    mensaje = "El campo 'Activo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                valor = valor.replace(",", "")

                if not validarEntero(ingreso):
                    mensaje = "El campo 'Ingreso' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(nomina):
                    mensaje = "El campo 'Planilla' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(tipo_pago):
                    mensaje = "El campo 'Tipo de Pago' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(tipo_contrato):
                    mensaje = "El campo 'Tipo de Contrato' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor):
                    mensaje = "El campo 'Valor' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(activo):
                    mensaje = "El campo 'Activo' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if ingreso == 0:
                    mensaje = "El registro del campo 'Ingreso' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if nomina == 0:
                    mensaje = "El registro del campo 'Nómina' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if tipo_pago == 0:
                    mensaje = "El registro del campo 'Tipo de Pago' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if tipo_contrato == 0:
                    mensaje = "El registro del campo 'Tipo de Contrato' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) > 18:
                    mensaje = (
                        "El campo 'Ingreso General' tiene como máximo 18 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if float(valor) == 0:
                    mensaje = "El campo 'Valor' debe ser mayor a cero (0)."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) < 0 and int(valor) > 2:
                    mensaje = "El valor del campo 'Activo' no es válido."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                fecha_valida = datetime.datetime.strptime(fecha_valida, "%d/%m/%Y")
                fecha_valida = datetime.datetime.strftime(fecha_valida, "%Y-%m-%d")

                vingreso = IngresoGeneral.objects.get(pk=ingreso)
                vnomina = Planilla.objects.get(pk=nomina)
                vtipopago = SalaryUnit.objects.get(pk=tipo_pago)
                vtipocontrato = TipoContrato.objects.get(pk=tipo_contrato)
                suc = Branch.objects.get(pk=request.session["sucursal"])
                oMd = IngresoGeneralDetalle.objects.get(pk=id)
                if oMd:
                    oMd.ingreso = vingreso
                    oMd.nomina = vnomina
                    oMd.tipo_pago = vtipopago
                    oMd.tipo_contrato = vtipocontrato
                    oMd.valor = valor
                    oMd.fecha_valida = fecha_valida
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def ingreso_general_detalle_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = IngresoGeneralDetalle.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------AJAX-------------------------------

# endregion

# region Código para Ingreso Individual


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_ingresoindividual", raise_exception=True)
def ingreso_individual_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_ingresoindividual"):
        lista = IngresoIndividual.objects.filter(empresa_reg=suc.empresa)
    else:
        lista = IngresoIndividual.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(request, "ingreso-individual-listado.html", {"lista": lista})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_ingresoindividual", raise_exception=True)
def ingreso_individual_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    tipos_ingresos = TipoIngreso.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(
        request, "ingreso-individual-form.html", {"tipos_ingresos": tipos_ingresos}
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_ingresoindividual", raise_exception=True)
def ingreso_individual_editar(request, id):
    dato = IngresoIndividual.objects.get(pk=id)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    tipos_ingresos = TipoIngreso.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(
        request,
        "ingreso-individual-form.html",
        {"dato": dato, "tipos_ingresos": tipos_ingresos, "editar": True},
    )


# ---------------------AJAX-------------------------------


def ingreso_individual_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                ingreso_i = request.POST["ingreso_i"]
                tipo_ingreso = request.POST["tipo_ingreso"]
                activo = int(request.POST["activo"])
                gravable = int(request.POST["gravable"])

                if len(ingreso_i) == 0:
                    mensaje = "El campo 'Ingreso Individual' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_ingreso) == 0:
                    mensaje = "El campo 'Tipo Ingreso' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if tipo_ingreso == 0:
                    mensaje = "El registro no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(ingreso_i) > 50:
                    mensaje = (
                        "El campo 'Ingreso Individual' tiene como máximo 50 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if gravable == 1:
                    gravable = True
                else:
                    gravable = False

                o_tipoingreso = TipoIngreso.objects.get(pk=tipo_ingreso)

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = IngresoIndividual(
                    ingreso_i=ingreso_i,
                    tipo_ingreso=o_tipoingreso,
                    gravable=gravable,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def ingreso_individual_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                ingreso_i = request.POST["ingreso_i"]
                tipo_ingreso = request.POST["tipo_ingreso"]
                activo = int(request.POST["activo"])
                gravable = int(request.POST["gravable"])

                if len(ingreso_i) == 0:
                    mensaje = "El campo 'Ingreso Individual' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_ingreso) == 0:
                    mensaje = "El campo 'Tipo Ingreso' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if tipo_ingreso == 0:
                    mensaje = "El registro no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(ingreso_i) > 50:
                    mensaje = (
                        "El campo 'Ingreso Individual' tiene como máximo 50 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if gravable == 1:
                    gravable = True
                else:
                    gravable = False

                o_tipoingreso = TipoIngreso.objects.get(pk=tipo_ingreso)
                oMd = IngresoIndividual.objects.get(pk=id)
                if oMd:
                    oMd.ingreso_i = ingreso_i
                    oMd.tipo_ingreso = o_tipoingreso
                    oMd.gravable = gravable
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def ingreso_individual_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = IngresoIndividual.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------AJAX-------------------------------

# endregion

# region Código para Ingreso Individual Detalle


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_ingresoindividualdetalle", raise_exception=True)
def ingreso_individual_detalle_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista = IngresoIndividualDetalle.objects.filter(sucursal_reg=suc, active=True)
    # if request.user.has_perm("worksheet.see_all_ingresoindividualdetalle"):
    #     lista = IngresoIndividualDetalle.objects.filter(empresa_reg=suc.empresa)
    # else:
    #     lista = IngresoIndividualDetalle.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(request, "ingreso-individual-detalle-listado.html", {"lista": lista})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_ingresoindividualdetalle", raise_exception=True)
def ingreso_individual_detalle_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    ingresos = IngresoIndividual.objects.filter(empresa_reg=suc.empresa, active=True)
    empleados = Employee.objects.filter(branch=suc, active=True).order_by("firstName")
    return render(
        request,
        "ingreso-individual-detalle-form.html",
        {"ingresos": ingresos, "empleados": empleados},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_ingresogeneraldetalle", raise_exception=True)
def ingreso_indidvidual_detalle_editar(request, id):
    dato = IngresoIndividualDetalle.objects.get(pk=id)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    ingresos = IngresoIndividual.objects.filter(empresa_reg=suc.empresa, active=True)
    empleados = Employee.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(
        request,
        "ingreso-individual-detalle-form.html",
        {"dato": dato, "ingresos": ingresos, "empleados": empleados, "editar": True},
    )


# ---------------------AJAX-------------------------------


def ingreso_indidvidual_detalle_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                ingreso_id = request.POST["ingreso"]
                empleado_id = request.POST["empleado"]
                valor = request.POST["valor"]
                fecha_valida = request.POST["fecha"]
                activo = request.POST["activo"]

                if len(ingreso_id) == 0:
                    mensaje = "El campo 'Ingreso' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(empleado_id) == 0:
                    mensaje = "El campo 'Empleado' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) == 0:
                    mensaje = "El campo 'Valor' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(fecha_valida) == 0:
                    mensaje = "El campo 'Válido hasta' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(activo) == 0:
                    mensaje = "El campo 'Activo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                valor = valor.replace(",", "")

                if not validarEntero(ingreso_id):
                    mensaje = "El campo 'Ingreso' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(empleado_id):
                    mensaje = "El campo 'Empleado' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor):
                    mensaje = "El campo 'Valor' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(activo):
                    mensaje = "El campo 'Activo' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if ingreso_id == 0:
                    mensaje = "El registro del campo 'Ingreso' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if empleado_id == 0:
                    mensaje = "El registro del campo 'Empleado' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) > 18:
                    mensaje = "El campo 'Valor' tiene como máximo 18 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if float(valor) == 0:
                    mensaje = "El campo 'Valor' debe ser mayor a cero (0)."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) < 0 and int(valor) > 2:
                    mensaje = "El valor del campo 'Activo' no es válido."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                vingreso = IngresoIndividual.objects.get(pk=ingreso_id)
                vempleado = Employee.objects.get(pk=empleado_id)
                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = IngresoIndividualDetalle(
                    ingreso=vingreso,
                    empleado=vempleado,
                    valor=valor,
                    fecha_valida=fecha_valida,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def ingreso_individual_detalle_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                ingreso_id = request.POST["ingreso"]
                empleado_id = request.POST["empleado"]
                valor = request.POST["valor"]
                fecha_valida = request.POST["fecha"]
                activo = request.POST["activo"]

                if len(ingreso_id) == 0:
                    mensaje = "El campo 'Ingreso' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(empleado_id) == 0:
                    mensaje = "El campo 'Empleado' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) == 0:
                    mensaje = "El campo 'Valor' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(fecha_valida) == 0:
                    mensaje = "El campo 'Válido hasta' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(activo) == 0:
                    mensaje = "El campo 'Activo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                valor = valor.replace(",", "")

                if not validarEntero(ingreso_id):
                    mensaje = "El campo 'Ingreso' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(empleado_id):
                    mensaje = "El campo 'Empleado' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor):
                    mensaje = "El campo 'Valor' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(activo):
                    mensaje = "El campo 'Activo' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if ingreso_id == 0:
                    mensaje = "El registro del campo 'Ingreso' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if empleado_id == 0:
                    mensaje = "El registro del campo 'Empleado' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) > 18:
                    mensaje = "El campo 'Valor' tiene como máximo 18 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if float(valor) == 0:
                    mensaje = "El campo 'Valor' debe ser mayor a cero (0)."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) < 0 and int(valor) > 2:
                    mensaje = "El valor del campo 'Activo' no es válido."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                vingreso = IngresoIndividual.objects.get(pk=ingreso_id)
                vempleado = Employee.objects.get(pk=empleado_id)
                suc = Branch.objects.get(pk=request.session["sucursal"])
                oMd = IngresoIndividualDetalle.objects.get(pk=id)
                if oMd:
                    oMd.ingreso = vingreso
                    oMd.empleado = vempleado
                    oMd.valor = valor
                    oMd.fecha_valida = fecha_valida
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def ingreso_individual_detalle_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = IngresoIndividualDetalle.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------AJAX-------------------------------

# endregion

# region Código para Ingreso Individual Planilla


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_ingresoindividualplanilla", raise_exception=True)
def ingreso_individual_planilla_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista = IngresoIndividualPlanilla.objects.filter(sucursal_reg=suc, active=True)
    # if request.user.has_perm("worksheet.see_all_ingresoindividualplanilla"):
    #     lista = IngresoIndividualPlanilla.objects.filter(empresa_reg=suc.empresa)
    # else:
    #     lista = IngresoIndividualPlanilla.objects.filter(empresa_reg=suc.empresa)
    return render(request, "ingreso-individual-planilla-listado.html", {"lista": lista})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_ingresoindividualplanilla", raise_exception=True)
def ingreso_individual_planilla_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    ingresos = IngresoIndividual.objects.filter(empresa_reg=suc.empresa, active=True)
    empleados = Employee.objects.filter(
        empresa_reg=suc.empresa, branch=suc, active=True
    )
    planillas = Planilla.objects.filter(sucursal_reg=suc, active=True)
    return render(
        request,
        "ingreso-individual-planilla-form.html",
        {"ingresos": ingresos, "empleados": empleados, "planillas": planillas},
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_ingresoindividualplanilla", raise_exception=True)
def ingreso_individual_planilla_editar(request, id):
    dato = IngresoIndividualPlanilla.objects.get(pk=id)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    ingresos = IngresoIndividual.objects.filter(empresa_reg=suc.empresa, active=True)
    empleados = Employee.objects.filter(empresa_reg=suc.empresa, active=True)
    planillas = Planilla.objects.filter(sucursal_reg=suc, active=True)
    return render(
        request,
        "ingreso-individual-planilla-form.html",
        {
            "dato": dato,
            "ingresos": ingresos,
            "empleados": empleados,
            "planillas": planillas,
            "editar": True,
        },
    )


# ---------------------AJAX-------------------------------


def ingreso_individual_planilla_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                ingreso_id = request.POST["ingreso"]
                empleado_id = request.POST["empleado"]
                planilla_id = request.POST["planilla"]
                valor = request.POST["valor"]
                activo = request.POST["activo"]

                if len(ingreso_id) == 0:
                    mensaje = "El campo 'Ingreso' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(empleado_id) == 0:
                    mensaje = "El campo 'Empleado' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(planilla_id) == 0:
                    mensaje = "El campo 'Planilla' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) == 0:
                    mensaje = "El campo 'Valor' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(activo) == 0:
                    mensaje = "El campo 'Activo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                valor = valor.replace(",", "")

                if not validarEntero(ingreso_id):
                    mensaje = "El campo 'Ingreso' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(empleado_id):
                    mensaje = "El campo 'Empleado' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(planilla_id):
                    mensaje = "El campo 'Planilla' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor):
                    mensaje = "El campo 'Valor' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(activo):
                    mensaje = "El campo 'Activo' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if ingreso_id == 0:
                    mensaje = "El registro del campo 'Ingreso' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if empleado_id == 0:
                    mensaje = "El registro del campo 'Empleado' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if planilla_id == 0:
                    mensaje = "El registro del campo 'Planilla' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) > 18:
                    mensaje = "El campo 'Valor' tiene como máximo 18 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if float(valor) == 0:
                    mensaje = "El campo 'Valor' debe ser mayor a cero (0)."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) < 0 and int(valor) > 2:
                    mensaje = "El valor del campo 'Activo' no es válido."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                vingreso = IngresoIndividual.objects.get(pk=ingreso_id)
                vempleado = Employee.objects.get(pk=empleado_id)
                vplanilla = Planilla.objects.get(pk=planilla_id)
                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = IngresoIndividualPlanilla(
                    ingreso=vingreso,
                    empleado=vempleado,
                    planilla=vplanilla,
                    valor=valor,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def ingreso_individual_planilla_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                ingreso_id = request.POST["ingreso"]
                empleado_id = request.POST["empleado"]
                planilla_id = request.POST["planilla"]
                valor = request.POST["valor"]
                activo = request.POST["activo"]

                if len(ingreso_id) == 0:
                    mensaje = "El campo 'Ingreso' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(empleado_id) == 0:
                    mensaje = "El campo 'Empleado' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(planilla_id) == 0:
                    mensaje = "El campo 'Planilla' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) == 0:
                    mensaje = "El campo 'Valor' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(activo) == 0:
                    mensaje = "El campo 'Activo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                valor = valor.replace(",", "")

                if not validarEntero(ingreso_id):
                    mensaje = "El campo 'Ingreso' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(empleado_id):
                    mensaje = "El campo 'Empleado' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(planilla_id):
                    mensaje = "El campo 'Planilla' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor):
                    mensaje = "El campo 'Valor' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarEntero(activo):
                    mensaje = "El campo 'Activo' es de tipo Numérico."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if ingreso_id == 0:
                    mensaje = "El registro del campo 'Ingreso' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if empleado_id == 0:
                    mensaje = "El registro del campo 'Empleado' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if planilla_id == 0:
                    mensaje = "El registro del campo 'Planilla' no existe."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor) > 18:
                    mensaje = "El campo 'Valor' tiene como máximo 18 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if float(valor) == 0:
                    mensaje = "El campo 'Valor' debe ser mayor a cero (0)."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) < 0 and int(valor) > 2:
                    mensaje = "El valor del campo 'Activo' no es válido."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                vingreso = IngresoIndividual.objects.get(pk=ingreso_id)
                vempleado = Employee.objects.get(pk=empleado_id)
                vplanilla = Planilla.objects.get(pk=planilla_id)
                suc = Branch.objects.get(pk=request.session["sucursal"])
                oMd = IngresoIndividualPlanilla.objects.get(pk=id)
                if oMd:
                    oMd.ingreso = vingreso
                    oMd.empleado = vempleado
                    oMd.planilla = vplanilla
                    oMd.valor = valor
                    oMd.active = activo

                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def ingreso_individual_planilla_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = IngresoIndividualPlanilla.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------AJAX-------------------------------

# endregion

# region Código para Planilla

@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_planilla", raise_exception=True)
def planilla_listado(request):

    suc = Branch.objects.get(pk=request.session["sucursal"])
    datos = Planilla.objects.filter(sucursal_reg=suc, active=True).order_by('-fecha_pago', 'pk')
    # if request.user.has_perm("worksheet.see_all_planilla"):
    #     datos = Planilla.objects.filter(empresa_reg=suc.empresa, active=True)
    # else:
    #     datos = Planilla.objects.filter(sucursal_reg=suc, active=True)
    return render(request, "planilla-listado.html", {"datos": datos})

@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_planilla", raise_exception=True)
def planilla_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    tipo_pago = SalaryUnit.objects.filter(empresa_reg=suc.empresa, active=True)
    tipo_planilla = TipoNomina.objects.filter(empresa_reg=suc.empresa, active=True)
    tipo_contrato = TipoContrato.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(
        request,
        "planilla-form.html",
        {
            "tipo_planilla": tipo_planilla,
            "tipos_pago": tipo_pago,
            "tipos_contrato": tipo_contrato,
        },
    )

@login_required(login_url="/form/iniciar-sesion/")
def planilla_registro_ver(request, id):
    datos = []
    l_ingresos = []
    l_deducciones_i = []
    l_deducciones_e = []
    datos2 = []
    datos3 = []
    datos4 = []
    datos5 = []
    datos6 = []
    ingresos = 0
    deducciones = 0
    suma_total_ingresos = 0
    suma_total_deducciones = 0
    suma_gingresos = 0
    suma_gdeducciones = 0
    suma_deducciones_i = 0
    suma_deducciones_e = 0
    suc = Branch.objects.filter(pk=request.session["sucursal"])
    planilla = Planilla.objects.get(pk=id)
    detalle_planilla = PlanillaDetalle.objects.filter(planilla__pk=planilla.id)
    for item in detalle_planilla:
        datos2 = []
        datos3 = []
        datos4 = []
        datos5 = []
        dias_trabajo = 0
        dias_trabajo = float(item.dias_salario) - float(item.dias_ausentes_sin_pago)
        total_salario = float(dias_trabajo) * float(item.salario_diario)

        ingresos = (
            PlanillaDetalleIngresos.objects.filter(
                planilla__pk=planilla.id, empleado=item.empleado
            )
            .values("empleado", "planilla", "ingreso")
            .annotate(Sum("valor"))
            .order_by("tipo_ingreso__indice_relevancia", "ingreso")
        )
        ingresos_agrupa = (
            PlanillaDetalleIngresos.objects.filter(
                planilla__pk=planilla.id, empleado=item.empleado
            )
            .values("tipo_ingreso__ingreso_tipo")
            .annotate(Sum("valor"))
            .order_by("tipo_ingreso__indice_relevancia", "tipo_ingreso__ingreso_tipo")
        )

        for item1 in ingresos:
            objeto1 = {
                "empleado": item.empleado,
                "planilla": planilla,
                "ingreso": item1["ingreso"],
                "valor": locale.format("%.2f", item1["valor__sum"], grouping=True),
            }
            datos2.append(objeto1)
            suma_total_ingresos += float(item1["valor__sum"])

        for item2 in ingresos_agrupa:
            objeto1 = {
                "ingreso": item2["tipo_ingreso__ingreso_tipo"],
                "valor": locale.format("%.2f", item2["valor__sum"], grouping=True),
            }
            datos4.append(objeto1)

        deducciones = (
            PlanillaDetalleDeducciones.objects.filter(
                planilla__pk=planilla.id, empleado=item.empleado
            )
            .values("empleado", "planilla", "deduccion")
            .annotate(Sum("valor"))
            .order_by("tipo_deduccion__indice_relevancia", "deduccion")
        )
        deducciones_agrupa = (
            PlanillaDetalleDeducciones.objects.filter(
                planilla__pk=planilla.id, empleado=item.empleado
            )
            .values("tipo_deduccion__deduccion_tipo")
            .annotate(Sum("valor"))
            .order_by("tipo_deduccion__indice_relevancia", "tipo_deduccion__deduccion_tipo")
        )

        for item2 in deducciones:
            o_empleado = Employee.objects.get(pk=item2["empleado"])
            objeto2 = {
                "empleado": o_empleado,
                "planilla": planilla,
                "deduccion": item2["deduccion"],
                "valor": locale.format("%.2f", item2["valor__sum"], grouping=True),
            }
            datos3.append(objeto2)
            suma_total_deducciones += float(item2["valor__sum"])

        for item2 in deducciones_agrupa:
            objeto1 = {
                "deduccion": item2["tipo_deduccion__deduccion_tipo"],
                "valor": locale.format("%.2f", item2["valor__sum"], grouping=True),
            }
            datos5.append(objeto1)

        objeto = {
            "id": item.pk,
            "empleado": item.empleado,
            "planilla": item.planilla,
            "salario_diario": item.salario_diario,
            "dias_ausentes_sin_pago": item.dias_ausentes_sin_pago,
            "dias_ausentes_con_pago": item.dias_ausentes_con_pago,
            "total_ingresos": locale.format(
                "%.2f", float(item.total_ingresos), grouping=True
            ),
            "total_deducciones": locale.format(
                "%.2f", item.total_deducciones, grouping=True
            ),
            "total_salario": locale.format("%.2f", total_salario, grouping=True),
            "salario_neto": locale.format(
                "%.2f",
                float(item.total_ingresos) - float(item.total_deducciones),
                grouping=True,
            ),
            "detalle_ingresos": datos2,
            "detalle_egresos": datos3,
            "ingresos_agrupa": datos4,
            "deducciones_agrupa": datos5,
        }
        datos.append(objeto)

    suma_total_neto = locale.format(
        "%.2f", suma_total_ingresos - suma_total_deducciones, grouping=True
    )
    suma_total_ingresos = locale.format("%.2f", suma_total_ingresos, grouping=True)
    suma_total_deducciones = locale.format(
        "%.2f", suma_total_deducciones, grouping=True
    )

    vingresos = (
        PlanillaDetalleIngresos.objects.filter(planilla=planilla)
        .values("ingreso")
        .annotate(Sum("valor"))
        .order_by("tipo_ingreso__indice_relevancia", "ingreso")
    )
    for ingreso in vingresos:
        suma_gingresos += float(ingreso["valor__sum"])
        dato = {
            "ingreso": ingreso["ingreso"],
            "valor": formato_millar(ingreso["valor__sum"]),
        }
        l_ingresos.append(dato)

    vdeducciones2 = (
        PlanillaDetalleDeducciones.objects.filter(planilla=planilla)
        .values("tipo_deduccion__deduccion_tipo", "tipo_deduccion__es_externa")
        .annotate(Sum("valor"))
        .order_by("tipo_deduccion__indice_relevancia", "tipo_deduccion__deduccion_tipo")
    )

    for fila in vdeducciones2:
        dato = {
            "deduccion": fila["tipo_deduccion__deduccion_tipo"],
            "valor": formato_millar(fila["valor__sum"]),
        }
        if fila["tipo_deduccion__es_externa"]:

            l_deducciones_e.append(dato)
            suma_deducciones_e += float(fila["valor__sum"])
        else:
            l_deducciones_i.append(dato)
            suma_deducciones_i += float(fila["valor__sum"])
        
        suma_gdeducciones += float(fila["valor__sum"])

    # for fila in vdeducciones2:
    #     l_deducciones = []
    #     vgrupo = fila["tipo_deduccion__deduccion_tipo"]
    #     vdeducciones = (
    #         PlanillaDetalleDeducciones.objects.filter(
    #             planilla=planilla, tipo_deduccion__deduccion_tipo=vgrupo
    #         )
    #         .values("deduccion")
    #         .annotate(Sum("valor"))
    #         .order_by("tipo_deduccion__indice_relevancia", "deduccion")
    #     )
    #     for deduccion in vdeducciones:
    #         dato = {
    #             "deduccion": deduccion["deduccion"],
    #             "valor": formato_millar(deduccion["valor__sum"]),
    #         }
    #         l_deducciones.append(dato)

    #     dato = {
    #         "grupo": vgrupo,
    #         "valor": formato_millar(fila["valor__sum"]),
    #         "detalle": l_deducciones,
    #     }
    #     l_gdeducciones.append(dato)
    #     suma_gdeducciones += float(fila["valor__sum"])

    # vdeducciones = PlanillaDetalleDeducciones.objects.filter(planilla=planilla).values('deduccion').annotate(Sum('valor')).order_by('tipo_deduccion__indice_relevancia', 'deduccion')

    # for deduccion in vdeducciones:
    #     suma_gdeducciones += float(deduccion["valor__sum"])
    #     dato = {
    #         'deduccion': deduccion["deduccion"],
    #         'valor':formato_millar(deduccion["valor__sum"])
    #     }
    #     l_deducciones.append(dato)
        

    return render(request, "planilla-ver.html", { "planilla": planilla, "detalle": datos, "ingresos": datos2, "deducciones": datos3, "suma_total_ingresos": suma_total_ingresos, "suma_total_deducciones": suma_total_deducciones,"suma_total_neto": suma_total_neto, "gingresos": l_ingresos, "gdeducciones_i": l_deducciones_i, "suma_ded_i":formato_millar(suma_deducciones_i), "gdeducciones_e": l_deducciones_e, "suma_ded_e": formato_millar(suma_deducciones_e), "sum_gingresos": formato_millar(suma_gingresos), "sum_gdeducciones": formato_millar(suma_gdeducciones)})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_planilla", raise_exception=True)
def planilla_editar(request, id):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    tipo_pago = SalaryUnit.objects.filter(empresa_reg=suc.empresa, active=True)
    tipo_planilla = TipoNomina.objects.filter(empresa_reg=suc.empresa, active=True)
    tipo_contrato = TipoContrato.objects.filter(empresa_reg=suc.empresa, active=True)
    o_planilla = Planilla.objects.get(pk=id)
    return render(
        request,
        "planilla-form.html",
        {
            "editar": True,
            "tipo_planilla": tipo_planilla,
            "tipos_pago": tipo_pago,
            "dato": o_planilla,
            "tipos_contrato": tipo_contrato,
        },
    )


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.play_planilla", raise_exception=True)
def planilla_generar(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    planillas = Planilla.objects.filter(sucursal_reg=suc, active=True, cerrada=False)
    return render(request, "planilla-generar.html", {"planillas": planillas})


# --------------------------------AJAX-----------------------------------


def obtener_empleados_planilla(request):
    try:
        mensaje = ""
        codigos = {}
        l_empleados = []
        if request.is_ajax():
            id = request.GET.get("id")
            if len(id) < 1:
                error = True
                mensaje = "Seleccione una planilla."
            else:
                id = int(id)
            if id == 0:
                error = True
                mensaje = "El registro no existe."
            else:
                tot_reg = Planilla.objects.filter(pk=id).count()
                if tot_reg > 0:
                    o_planilla = Planilla.objects.get(pk=id)
                    suc = Branch.objects.get(pk=request.session["sucursal"])
                    empleados = Employee.objects.filter(
                        active=True,
                        tipo_nomina=o_planilla.tipo_planilla,
                        salaryUnits=o_planilla.frecuencia_pago,
                        branch=suc,
                    )
                    if empleados.count() > 0:
                        for item in empleados:
                            codigo = {"ID": item.pk}
                            l_empleados.append(codigo)
                        error = False
                        data = {"error": error, "empleados": l_empleados}
                        return JsonResponse(data)
                    else:
                        data = {
                            "error": True,
                            "mensaje": "No encontraron empleados pertenecientes a la planilla.",
                        }
                        return JsonResponse(data)
                else:
                    error = True
                    mensaje = "No existe el registro."
        else:
            error = True
            mensaje = "El método no está permitido."
        data = {"error": error, "mensaje": mensaje}
        return JsonResponse(data)
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": "Error",
        }
        return JsonResponse(data)


def planilla_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = request.POST["id"]
                tipo_planilla_id = request.POST["tipo_planilla"]
                tipo_pago_id = request.POST["tipo_pago"]
                tipo_contrato_id = request.POST["tipo_contrato"]
                fecha_pago = request.POST["fecha_pago"]
                fecha_inicio = request.POST["fecha_inicio"]
                fecha_fin = request.POST["fecha_fin"]
                descripcion = request.POST["descripcion"]
                chk_especial = request.POST["especial"]
                chk_dedrap = request.POST["ded_rap"]
                chk_dedisr = request.POST["ded_isr"]
                chk_dedimv = request.POST["ded_imv"]

                if int(tipo_planilla_id) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Tipo de Planilla" es obligatorio.',
                        }
                    )
                else:
                    tipos_planilla = TipoNomina.objects.filter(pk=tipo_planilla_id)
                    if tipos_planilla.count() > 0:
                        o_tipo_planilla = TipoNomina.objects.get(pk=tipo_planilla_id)
                    else:
                        return JsonResponse(
                            {"error": True, "mensaje": "El Tipo de Planilla no existe."}
                        )

                if int(tipo_pago_id) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Tipo de Pago" es obligatorio.',
                        }
                    )
                else:
                    tipos_pago = SalaryUnit.objects.filter(pk=tipo_pago_id)
                    if tipos_pago.count() > 0:
                        o_tipo_pago = SalaryUnit.objects.get(pk=tipo_pago_id)
                    else:
                        return JsonResponse(
                            {"error": True, "mensaje": "El Tipo de Pago no existe."}
                        )

                if int(tipo_contrato_id) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Tipo de Contrato" es obligatorio.',
                        }
                    )
                else:
                    tipos_contrato = TipoContrato.objects.filter(pk=tipo_contrato_id)
                    if tipos_contrato.count() > 0:
                        o_tipo_contrato = TipoContrato.objects.get(pk=tipo_contrato_id)
                    else:
                        return JsonResponse(
                            {"error": True, "mensaje": "El Tipo de Contrato no existe."}
                        )

                if len(fecha_pago) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Fecha de Pago" es obligatorio.',
                        }
                    )

                if len(fecha_inicio) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Fecha de Inicio" es obligatorio.',
                        }
                    )

                if len(fecha_fin) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Fecha de Fin" es obligatorio.',
                        }
                    )

                if len(descripcion) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Descripcion" es obligatorio.',
                        }
                    )

                tot_reg = Planilla.objects.filter(pk=id).count()
                if tot_reg > 0:
                    o_Mdl = Planilla.objects.get(pk=id)
                    if o_Mdl.cerrada:
                        return JsonResponse(
                            {"error": True, "mensaje": "La planilla ya está cerrada."}
                        )
                    o_Mdl.tipo_planilla = o_tipo_planilla
                    o_Mdl.frecuencia_pago = o_tipo_pago
                    o_Mdl.tipo_contrato = o_tipo_contrato
                    o_Mdl.fecha_pago = fecha_pago
                    o_Mdl.fecha_inicio = fecha_inicio
                    o_Mdl.fecha_fin = fecha_fin
                    o_Mdl.descripcion = descripcion
                    o_Mdl.especial = chk_especial
                    o_Mdl.rap = chk_dedrap
                    o_Mdl.isr = chk_dedisr
                    o_Mdl.imv = chk_dedimv
                    o_Mdl.save()
                    return JsonResponse(
                        {"error": False, "mensaje": "Se ha guardado el registro."}
                    )
                else:
                    return JsonResponse(
                        {"error": True, "mensaje": "El registro no existe."}
                    )
            else:
                return JsonResponse(
                    {"error": True, "mensaje": "El método no está permitido."}
                )
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
            return JsonResponse(data)
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": "Error",
        }
        return JsonResponse(data)


def planilla_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                tipo_planilla_id = request.POST["tipo_planilla"]
                tipo_pago_id = request.POST["tipo_pago"]
                tipo_contrato_id = request.POST["tipo_contrato"]
                fecha_pago = request.POST["fecha_pago"]
                fecha_inicio = request.POST["fecha_inicio"]
                fecha_fin = request.POST["fecha_fin"]
                descripcion = request.POST["descripcion"]
                chk_especial = request.POST["especial"]
                # chk_dedisr = request.POST["ded_isr"]
                # chk_dedimv = request.POST["ded_imv"]

                if int(tipo_planilla_id) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Tipo de Planilla" es obligatorio.',
                        }
                    )
                else:
                    tipos_planilla = TipoNomina.objects.filter(pk=tipo_planilla_id)
                    if tipos_planilla.count() > 0:
                        o_tipo_planilla = TipoNomina.objects.get(pk=tipo_planilla_id)
                    else:
                        return JsonResponse(
                            {"error": True, "mensaje": "El Tipo de Planilla no existe."}
                        )

                if int(tipo_pago_id) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Tipo de Pago" es obligatorio.',
                        }
                    )
                else:
                    tipos_pago = SalaryUnit.objects.filter(pk=tipo_pago_id)
                    if tipos_pago.count() > 0:
                        o_tipo_pago = SalaryUnit.objects.get(pk=tipo_pago_id)
                    else:
                        return JsonResponse(
                            {"error": True, "mensaje": "El Tipo de Pago no existe."}
                        )

                if int(tipo_contrato_id) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Tipo de Contrato" es obligatorio.',
                        }
                    )
                else:
                    tipos_contrato = TipoContrato.objects.filter(pk=tipo_contrato_id)
                    if tipos_contrato.count() > 0:
                        o_tipo_contrato = TipoContrato.objects.get(pk=tipo_contrato_id)
                    else:
                        return JsonResponse(
                            {"error": True, "mensaje": "El Tipo de Contrato no existe."}
                        )

                if len(fecha_pago) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Fecha de Pago" es obligatorio.',
                        }
                    )

                if len(fecha_inicio) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Fecha de Inicio" es obligatorio.',
                        }
                    )

                if len(fecha_fin) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Fecha de Fin" es obligatorio.',
                        }
                    )

                if len(descripcion) == 0:
                    return JsonResponse(
                        {
                            "error": True,
                            "mensaje": 'El campo "Descripcion" es obligatorio.',
                        }
                    )

                suc = Branch.objects.get(pk=request.session["sucursal"])
                oPlanilla = Planilla(
                    correlativo=1,
                    tipo_planilla=o_tipo_planilla,
                    tipo_contrato=o_tipo_contrato,
                    descripcion=descripcion,
                    frecuencia_pago=o_tipo_pago,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    fecha_pago=fecha_pago,
                    especial=chk_especial,
                    rap=False,
                    isr=False,
                    imv=False,
                    cerrada=False,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    active=True,
                    user_reg=request.user,
                )

                oPlanilla.save()
                return JsonResponse(
                    {
                        "error": False,
                        "mensaje": "Se ha guardado el registro de Planilla.",
                    }
                )
            else:
                return JsonResponse(
                    {"error": True, "mensaje": "El método no está permitido."}
                )
        else:
            pass
        return JsonResponse({"error": False, "mensaje": "Respuesta exitosa"})
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": str(ex),
        }
        return JsonResponse(data)


def planilla_generar_calculos(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                if not "sucursal" in request.session:
                    data = {"error": True, "mensaje": "Su sesión ha caducado"}
                    return JsonResponse(data)
                planilla_id = request.POST["id"]
                if len(planilla_id) == 0:
                    data = {
                        "error": True,
                        "mensaje": "No se pasó ningún parámetro de planilla.",
                    }
                    return JsonResponse(data)
                else:
                    if validarEntero(planilla_id):
                        tot_reg = Planilla.objects.filter(pk=planilla_id).count()
                        if tot_reg > 0:
                            suc = Branch.objects.get(pk=request.session["sucursal"])
                            o_planilla = Planilla.objects.get(pk=planilla_id)
                            empleados = Employee.objects.filter(tipo_nomina=o_planilla.tipo_planilla,tipo_contrato=o_planilla.tipo_contrato, salaryUnits=o_planilla.frecuencia_pago, active=True,branch=suc).order_by("firstName")

                            detalles_planillas_deducciones = PlanillaDetalleDeducciones.objects.filter(planilla=o_planilla)
                            if detalles_planillas_deducciones.count() > 0:
                                detalles_planillas_deducciones.delete()

                            detalles_planillas = PlanillaDetalle.objects.filter(planilla=o_planilla)
                            if detalles_planillas.count() > 0:
                                detalles_planillas.delete()

                            regs_planilla_ingresos = PlanillaDetalleIngresos.objects.filter(planilla=o_planilla)
                            
                            if regs_planilla_ingresos.count() > 0:
                                regs_planilla_ingresos.delete()

                            regs_control_saldo = ControlPagosDeduccionIndividual.objects.filter(planilla=o_planilla)
                            
                            if regs_control_saldo.count() > 0:
                                regs_control_saldo.delete()

                            # regs_plan_det_ded_det = DetallePlanillaDetalleDeduccion.objects.filter(planilla_detalle_ded__planilla=o_planilla)
                            
                            # if regs_plan_det_ded_det.count() > 0:
                            #     regs_plan_det_ded_det.delete()

                            for item in empleados:
                                tipos_deducciones = []
                                comentario = ""
                                tigi = 0
                                tigg = 0
                                tigp = 0
                                tii = 0
                                tig = 0
                                tip = 0
                                tihss = 0
                                sbb = 0

                                tot_ded_ind = 0

                                tot_ind_ded = 0
                                tot_ingreso = 0
                                tot_deducciones = 0
                                tot_ind_ing = 0
                                tot_gen_ing = 0
                                tot_gen_ded = 0
                                tot_pla_ing = 0
                                tot_pla_ded = 0
                                tot_dias_sin_pago = 0
                                total_dias_trabajados = 0
                                salario_diario = 0
                                total_ingreso = 0
                                total_egreso = 0
                                dias_ausencia_con_pago = 0
                                dias_ausencia_sin_pago = 0
                                deduccion_ihss = 0
                                deduccion_rap = 0
                                deduccion_isr = 0
                                deduccion_vec = 0
                                total_rap = 0
                                tpagos = 0
                                res_fec = 0
                                salario_diario = float(item.salario_diario)
                                total_dias_trabajados = int(item.salaryUnits.dias_salario)
                                #Q(fecha_fin__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin)) | Q(fecha_inicio__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin), fecha_fin__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin)) | Q(fecha_inicio__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin))

                                # contratos = Contrato.objects.filter(Q(empleado=item) & Q(fecha_fin__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin)) & (Q(fecha_inicio__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin), fecha_fin__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin)) | Q(fecha_inicio__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin))) & Q(active=True))
                                contratos = Contrato.objects.filter(Q(empleado=item, active=True, fecha_fin__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin)) | Q(empleado=item, active=True, fecha_inicio__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin), fecha_fin__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin)) | Q(empleado=item, active=True, fecha_inicio__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin)))
                                #contratos = Contrato.objects.filter(Q(empleado=item, active=True) & (Q(fecha_inicio__)))

                                res_dia_trab = 0
                                res_dia_plan = 0
                                res_dia_plan =+ (o_planilla.fecha_fin - o_planilla.fecha_inicio).days + 1
                                # if res_dia_plan < o_planilla.frecuencia_pago.dias_salario:
                                #     datee = datetime.datetime.strptime(o_planilla.fecha_inicio, "%Y-%m-%d")
                                #     if datee.month == 2:
                                #         res_dia_plan = total_dias_trabajados

                                if contratos.count() > 0:
                                    for contrato in contratos:
                                        v_fecha_final = contrato.fecha_fin
                                        # En este apartado se verifica si el empleado tiene un valor en el campo termDate que
                                        # determina la fecha que el empleado finalizo su relación laboral con la empresa
                                        if item.termDate:
                                            # Se procede a evaluar si la fecha de finalización del empleado es mayor
                                            # a la fecha final de contrato
                                            if item.termDate >= o_planilla.fecha_inicio and item.termDate <= o_planilla.fecha_fin:
                                                if item.termDate >= contrato.fecha_fin:
                                                    v_fecha_final = contrato.fecha_fin # Se asigna como fecha final la fecha de contrato
                                                else:
                                                    v_fecha_final = item.termDate
                                            else:
                                                v_fecha_final = contrato.fecha_fin
                                                # Se asigna como fecha final el valor que está en la información del empleado
                                        else:
                                            v_fecha_final = contrato.fecha_fin # Se asigna como fecha final el valor final de contrato en caso que en la info del empleado no tenga fecha final

                                        #Se evalúa si la fecha que iniciar contrato y finaliza relación laboral estan dentro del rango de fecha de la planilla
                                        if contrato.fecha_inicio >= o_planilla.fecha_inicio and v_fecha_final <= o_planilla.fecha_fin:
                                            #Se suma a resultado de dias trabajados el restante entre la fecha final de la relación profesional y
                                            #la fecha de inicio del contrato
                                            res_dia_trab += (v_fecha_final - contrato.fecha_inicio).days + 1
                                            
                                        #Se evalúa si la fecha inicio de contrato es antes que la fecha inicio de planilla y la fecha final de
                                        #relación profesional está entre el rango de fecha de inicio y final de planilla
                                        if contrato.fecha_inicio < o_planilla.fecha_inicio and (v_fecha_final >= o_planilla.fecha_inicio and v_fecha_final <= o_planilla.fecha_fin):
                                            #Se suma a resultado de dias trabajados el restante entre la fecha final de la relación profesional y
                                            #la fecha de incio de la planilla
                                            res_dia_trab += (v_fecha_final - o_planilla.fecha_inicio).days + 1

                                        #Se evalúa si la fecha final de relación profesional es después de la fecha final de la planilla y
                                        #la fecha inicial del contrato es entre el rango de fecha inicial y final de la planilla
                                        if v_fecha_final > o_planilla.fecha_fin and (contrato.fecha_inicio >= o_planilla.fecha_inicio and contrato.fecha_inicio <= o_planilla.fecha_fin):
                                            #Se suma a resultado de dias trabajados el restante entre la final de planilla y la fecha inicio de contrato
                                            res_dia_trab += (o_planilla.fecha_fin - contrato.fecha_inicio).days + 1
                                            if res_dia_trab < total_dias_trabajados:
                                                res_dia_trab = total_dias_trabajados
                                
                                #Si el empleado no tiene contratos pero si tiene una fecha de finalización de relación profesional
                                elif item.termDate:
                                    #Se toma como fecha final el campo termDate del maestro de empleados
                                    v_fecha_final = item.termDate
                                    #Se evalua si la fecha final está entre el rango de fecha inicial y final de la planilla
                                    if v_fecha_final >= o_planilla.fecha_inicio and v_fecha_final <= o_planilla.fecha_fin:
                                        #Se suma a resultado de dias trabajados el restante entre la fecha final y la fecha inicial de planilla
                                        res_dia_trab += (v_fecha_final - o_planilla.fecha_inicio).days + 1
                                
                                #res_fec += res_dia_plan - res_dia_trab
                                res_fec += total_dias_trabajados - res_dia_trab
                                
                                # if item.startDate:
                                #     res_fec += (item.startDate - o_planilla.fecha_inicio).days
                                if res_fec >= 0:
                                    # total_dias_trabajados = total_dias_trabajados - res_fec
                                    if res_fec < total_dias_trabajados:
                                        dias_ausencia_sin_pago = dias_ausencia_sin_pago + res_fec
                                else:
                                    res_fec = 0

                                # if item.termDate:
                                #     res_fec += (o_planilla.fecha_fin - item.termDate).days
                                # if res_fec >= 0:
                                #     if res_fec < total_dias_trabajados:
                                #         dias_ausencia_sin_pago = dias_ausencia_sin_pago + res_fec
                                # else:
                                #     res_fec = 0

                                salario_mensual = salario_diario * 30
                                total_ingreso = total_dias_trabajados * salario_diario
                                if res_fec > 0:
                                    valor_sueldo = (total_dias_trabajados - dias_ausencia_sin_pago) * salario_diario
                                else:
                                    valor_sueldo = (total_dias_trabajados * salario_diario)

                                d_ingresos = IngresoEmpleado.objects.filter(empleado=item, planilla=o_planilla)
                                for d_ingreso in d_ingresos:
                                    tot_ingreso += d_ingreso.monto
                                    GuardarDetalleIngreso(
                                        item,
                                        o_planilla,
                                        d_ingreso.ingreso.ingreso_tipo,
                                        d_ingreso.ingreso,
                                        d_ingreso.monto,
                                        suc.empresa,
                                        suc,
                                        request.user,
                                    )
                                    # GuardarDetalleDeduccionIngreso(1, d_ingreso.ingreso.ingreso_tipo, d_ingreso.monto, item, o_planilla, suc.empresa, suc, request.user, d_ingreso.ingreso, False, 0)
                                # Ingreso Individual Detalle
                                # ingresos_individuales = IngresoIndividualDetalle.objects.filter(empleado=item, fecha_valida__gte=o_planilla.fecha_inicio, fecha_valida__lte=o_planilla.fecha_fin, active=True)
                                # ingresos_individuales = IngresoIndividualDetalle.objects.filter(empleado=item, fecha_valida__gte=o_planilla.fecha_inicio, active=True)
                                # for item1 in ingresos_individuales:
                                #     if item1.ingreso.gravable:
                                #         tigi += item1.valor
                                #     else:
                                #         tii += item1.valor
                                #     GuardarDetalleDeduccionIngreso(1, item1.ingreso.ingreso_i, item1.valor, item, o_planilla, suc.empresa, suc, request.user, item1.ingreso.tipo_ingreso, False, 0)

                                # Ingreso general
                                # ingresos_generales = IngresoGeneralDetalle.objects.filter(nomina=o_planilla, tipo_pago=o_planilla.frecuencia_pago, tipo_contrato=item.tipo_contrato, fecha_valida__gte=o_planilla.fecha_inicio, fecha_valida__lte=o_planilla.fecha_fin, active=True)
                                # ingresos_generales = IngresoGeneralDetalle.objects.filter(nomina=o_planilla, tipo_pago=o_planilla.frecuencia_pago, tipo_contrato=item.tipo_contrato, fecha_valida__gte=o_planilla.fecha_inicio, active=True)
                                # for item2 in ingresos_generales:
                                #     if item2.ingreso.gravable:
                                #         tigg += item2.valor
                                #     else:
                                #         tig += item2.valor
                                #     GuardarDetalleDeduccionIngreso(1, item2.ingreso.ingreso_g, item2.value, item, o_planilla, suc.empresa, suc, request.user, item2.ingreso.tipo_ingreso, False, 0)

                                # Ingreso Individual Planilla
                                # ingresos_planilla = IngresoIndividualPlanilla.objects.filter(empleado=item, planilla=o_planilla, active=True)
                                # for item3 in ingresos_planilla:
                                #     if item3.ingreso.gravable:
                                #         tigp += item3.valor
                                #     else:
                                #         tip += item3.valor
                                #     GuardarDetalleDeduccionIngreso(1, item3.ingreso.ingreso_i, item3.valor, item, o_planilla, suc.empresa, suc, request.user, item3.ingreso.tipo_ingreso, False, 0)

                                # tot_pla_ing = float(tigi) + float(tii) + float(tigg) + float(tig) + float(tigp) + float(tip)
                                tot_pla_ing = float(tot_ingreso)
                                ausencias_con_pago = Ausentismo.objects.filter(Q(desde__range=(o_planilla.fecha_inicio,o_planilla.fecha_fin)) | Q(hasta__range=(o_planilla.fecha_inicio,o_planilla.fecha_fin)) | Q(desde__lt=o_planilla.fecha_inicio, hasta__gt=o_planilla.fecha_fin), empleado=item,sucursal_reg=suc, motivo__pagado=True, active=True)
                                if ausencias_con_pago.count() > 0:
                                    dias_ausencia_con_pago = 1
                                    dias_ausencia_en_pla = 1
                                    tot_ajuste_lempiras = 0
                                    for item1 in ausencias_con_pago:
                                        dias_ausencia = 1
                                        tpagos = 0
                                        dias_ausencia = (dias_ausencia + (item1.hasta - item1.desde).days)
                                        dias_ausencia_con_pago = (dias_ausencia_con_pago + (item1.hasta - item1.desde).days)
                                        dias_normales = 0
                                        dias_ajustes = 0
                                        tot_dias_ajuste = 0
                                        ajustes = SeguroSocialAjuste.objects.filter(empresa_reg=suc.empresa, active=True)
                                        if ajustes.count() > 0:
                                            o_ajustes = ajustes[0]
                                            if dias_ausencia > int(o_ajustes.maximo_dias):
                                                if (item1.desde >= o_planilla.fecha_inicio and item1.hasta <= o_planilla.fecha_fin):
                                                    dias_ausencia = 1
                                                    tot_dias_planilla = ( dias_ausencia + (item1.hasta - item1.desde).days)
                                                    if tot_dias_planilla > int(o_ajustes.maximo_dias):
                                                        tot_dias_ajuste = tot_dias_planilla - int(o_ajustes.maximo_dias)
                                                    

                                                if (item1.desde < o_planilla.fecha_inicio and item1.hasta <= o_planilla.fecha_fin):
                                                    tot_dias_planilla = 1
                                                    tot_dias_planilla = (tot_dias_planilla + (item1.hasta - o_planilla.fecha_inicio).days)
                                                    tot_dias = (dias_ausencia_con_pago - tot_dias_planilla)
                                                    #Si el total de días es mayor que el maximo de días, entonces no se pagará dias
                                                    #completos en la planilla del ciclo
                                                    if tot_dias > int(o_ajustes.maximo_dias):
                                                        tot_dias_ajuste = tot_dias_planilla
                                                    else:
                                                        tot_dias_n = (int(o_ajustes.maximo_dias) - tot_dias)
                                                        tot_dias_ajuste = tot_dias_planilla - tot_dias_n
                                                    # tot_dias = (int(o_ajustes.maximo_dias) - tot_dias)
                                                    # tot_dias_planilla = (tot_dias_planilla - tot_dias)
                                                    # if tot_dias_planilla > int(item.salaryUnits.dias_salario):
                                                    #     tot_dias_planilla = int(item.salaryUnits.dias_salario)
                                                    #     tot_dias_ajuste = (tot_dias_planilla)

                                                if (item1.desde < o_planilla.fecha_inicio and item1.hasta > o_planilla.fecha_fin):
                                                    tot_dias_planilla = 1
                                                    tot_dias_planilla = (tot_dias_planilla + (o_planilla.fecha_fin - o_planilla.fecha_inicio).days)
                                                    tot_dias_resta = (1 + (o_planilla.fecha_fin - item1.desde).days)
                                                    tot_dias_resta = (tot_dias_resta - tot_dias_planilla)
                                                    if tot_dias_resta > int(o_ajustes.maximo_dias):
                                                        tot_dias_ajuste = tot_dias_planilla
                                                    else:
                                                        tot_dias_resta = (int(o_ajustes.maximo_dias) - tot_dias_resta)
                                                        tot_dias_planilla = (tot_dias_planilla - tot_dias_resta)
                                                        tot_dias_ajuste = tot_dias_planilla

                                                if (item1.desde >= o_planilla.fecha_inicio and item1.hasta > o_planilla.fecha_fin):
                                                    tot_dias_planilla = 1
                                                    tot_dias_planilla = (tot_dias_planilla + (o_planilla.fecha_fin - item1.desde).days)
                                                    if tot_dias_planilla > int(o_ajustes.maximo_dias):
                                                        tot_dias_planilla = (tot_dias_planilla - int(o_ajustes.maximo_dias))
                                                        tot_dias_ajuste = (tot_dias_planilla)

                                                tot_ajuste = tot_dias_ajuste * (salario_diario * ((100 - float(o_ajustes.porcentaje)) / 100))
                                                # print("Entro a maximo de dias")
                                                # print(valor_sueldo)
                                                # print(tot_ajuste)
                                                # print(tot_dias_ajuste)
                                                # print(item.firstName)
                                                # print(item.middleName)
                                                valor_sueldo = valor_sueldo - tot_ajuste
                                                # tot_ajuste_lempiras += tot_ajuste
                                                # total_ingreso = total_ingreso - tot_ajuste
                                                # total_egreso = total_egreso + tot_ajuste_lempiras
                                                # comentario = "Su salario ha disminuido por concepto de ausencia médica que cubre el IHSS"
                                                # GuardarDetalleDeduccionIngreso(
                                                #     2,
                                                #     "Deducción de salario por incapacidad cubierta por IHSS",
                                                #     tot_ajuste,
                                                #     item,
                                                #     o_planilla,
                                                #     suc.empresa,
                                                #     suc,
                                                #     request.user,
                                                #     None,
                                                #     None,
                                                #     None
                                                # )
                                
                                # deduccion_ihss = 0
                                # if EmpleadoDeducciones.objects.filter(deduccion='IHSS', empleado=item).exists():
                                #     if TipoDeduccion.objects.filter(grupo="IHSS").exists():
                                #         o_grup = TipoDeduccion.objects.get(grupo="IHSS")
                                #         tipos_ihss = SeguroSocial.objects.filter(active=True)
                                #         for item_21 in tipos_ihss:
                                #             if salario_mensual > float(item_21.techo):
                                #                 salario_mensual = float(item_21.techo)
                                #             deduccion_ihss = deduccion_ihss + ((salario_diario * 30) * (float(item_21.porcentaje_e) / 100))

                                #         tipo_deduccion = {'nombre': 'IHSS', 'valor': deduccion_ihss, 'orden': o_grup.orden}
                                #         tipos_deducciones.append(tipo_deduccion)

                                # ausencias_sin_pago = Ausentismo.objects.filter(Q(desde__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin)) | Q(hasta__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin)) | Q(desde__gt=o_planilla.fecha_inicio, hasta__lt=o_planilla.fecha_fin), empleado=item, sucursal_reg=suc, motivo__pagado=False, active=True)
                                # ausencias_sin_pago = Ausentismo.objects.filter(
                                #     desde__gte=o_planilla.fecha_inicio,
                                #     hasta__lte=o_planilla.fecha_fin,
                                #     empleado=item,
                                #     sucursal_reg=suc,
                                #     motivo__pagado=False,
                                #     active=True,
                                # )
                                ausencias_sin_pago = Ausentismo.objects.filter(empleado=item, fecha_aplica__range=(o_planilla.fecha_inicio, o_planilla.fecha_fin), sucursal_reg=suc, motivo__pagado=False, active=True)
                                if ausencias_sin_pago.count() > 0:
                                    
                                    for ausencia in ausencias_sin_pago:
                                        dias_ausencia_sin_pago = (dias_ausencia_sin_pago + 1)
                                        dias_ausencia_sin_pago = (dias_ausencia_sin_pago + (ausencia.hasta - ausencia.desde).days)
                                        valor_sueldo = valor_sueldo - (((ausencia.hasta - ausencia.desde).days + 1) * salario_diario)
                                        tot_dias_sin_pago += dias_ausencia_sin_pago
                                    #GuardarDetalleDeduccionIngreso(2, "Ausencias no justificadas", dias_ausencia_sin_pago * salario_diario, item, o_planilla, suc.empresa, suc, request.user, None)
                                    

                                    # o_planilla_detalle_deduccion = PlanillaDetalleDeducciones(
                                    #     empleado = item,
                                    #     planilla = o_planilla,
                                    #     deduccion = "Ausencia no justificada",
                                    #     valor = tot_dias_sin_pago * salario_diario,
                                    #     empresa_reg = suc.empresa,
                                    #     sucursal_reg = suc,
                                    #     user_reg = request.user
                                    # )
                                    # o_planilla_detalle_deduccion.save()

                                # #if o_planilla.ihss:
                                #     dedaplicada = EmpleadoDeducciones.objects.filter(empleado=item, empresa_reg=suc.empresa, deduccion='IHSS', active=True)
                                #     if dedaplicada.count() > 0:
                                #         tipos_ihss = SeguroSocial.objects.filter(empresa_reg=suc.empresa, active=True)
                                #         sbb = salario_mensual + tigi + tigg + tigp

                                #         for item4 in tipos_ihss:
                                #             if sbb > float(item4.techo):
                                #                 sbb = float(item4.techo)
                                #             deduccion_ihss = deduccion_ihss + (sbb * (float(item4.porcentaje_e) / 100))
                                #             if item.extEmpNo == 'DARO':
                                #                     print(sbb)

                                #         deduccion_tipo = TipoDeduccion.objects.filter(tipo_deduccion='IHSS', empresa_reg=suc.empresa, active=True)
                                #         if deduccion_tipo.count() > 0:
                                #             orden = int(deduccion_tipo[0].orden)
                                #         else:
                                #             orden = 0
                                #         if deduccion_ihss > 0:
                                #             tipo_deduccion = {'nombre': 'IHSS', 'valor': deduccion_ihss, 'orden': orden}
                                #             tipos_deducciones.append(tipo_deduccion)

                                # #v_rap = 0
                                # if o_planilla.rap:
                                #     dedaplicada = EmpleadoDeducciones.objects.filter(empleado=item, empresa_reg=suc.empresa, deduccion='RAP', active=True)
                                #     if dedaplicada.count() > 0:
                                #         sbb = salario_mensual + tigi + tigg + tigp
                                #         tipos_rap = RapDeduccion.objects.filter(empresa_reg=suc.empresa, active=True)
                                #         for item5 in tipos_rap:
                                #             if sbb > float(item5.techo):
                                #                 sbb = sbb - float(item5.techo)
                                #             deduccion_rap = deduccion_rap + (sbb * (float(item5.porcentaje)/100))
                                #         deduccion_tipo = TipoDeduccion.objects.filter(tipo_deduccion='RAP', empresa_reg=suc.empresa, active=True)
                                #         if deduccion_tipo.count() > 0:
                                #             orden = int(deduccion_tipo[0].orden)
                                #         else:
                                #             orden = 0

                                #         if deduccion_rap > 0:
                                #             tipo_deduccion = {'nombre': 'RAP', 'valor': deduccion_rap, 'orden': orden}
                                #             tipos_deducciones.append(tipo_deduccion)

                                # #if o_planilla.isr:
                                #     dedaplicada = EmpleadoDeducciones.objects.filter(empleado=item, empresa_reg=suc.empresa, deduccion='ISR', active=True)
                                #     if dedaplicada.count() > 0:
                                #         sbb = float(salario_mensual) + float(tigi) + float(tigg) + float(tigp)
                                #         isr_encabezados = EncabezadoImpuestoSobreRenta.objects.filter(empresa_reg=suc.empresa, active=True).order_by('-id')
                                #         if isr_encabezados.count() > 0:
                                #             o_encabezadoisr = isr_encabezados[0]
                                #             deduccion_tipo = TipoDeduccion.objects.filter(tipo_deduccion='ISR', empresa_reg=suc.empresa, active=True)
                                #             if deduccion_tipo.count() > 0:
                                #                 orden = int(deduccion_tipo[0].orden)
                                #             else:
                                #                 orden = 0

                                #             isr_detalles = ImpuestoSobreRenta.objects.filter(encabezado__pk=o_encabezadoisr.pk, active=True).order_by('id')
                                #             sueldo_anual = (salario_diario * 30) * 14

                                #             registro_i = 1
                                #             for item_detalle in isr_detalles:
                                #                 if registro_i == 1:
                                #                     if o_encabezadoisr.valor:
                                #                         item_detalle.hasta = float(item_detalle.hasta) + float(o_encabezadoisr.valor)
                                #                     if o_encabezadoisr.valor1:
                                #                         item_detalle.hasta = float(item_detalle.hasta) + float(o_encabezadoisr.valor1)
                                #                     if o_encabezadoisr.valor2:
                                #                         item_detalle.hasta = float(item_detalle.hasta) + float(o_encabezadoisr.valor2)

                                #                 if sueldo_anual > 0:
                                #                     deduccion_isr += sueldo_anual * (float(item_detalle.porcentaje) / 100)
                                #                     sueldo_anual = float(sueldo_anual) - float(item_detalle.hasta)
                                #                 else:
                                #                     deduccion_isr += 0
                                #                 registro_i += 1

                                #             if item.salaryUnits.dias_salario:
                                #                 tpagos = int(30 / item.salaryUnits.dias_salario)
                                #                 tpagos = tpagos * 12

                                #                 deduccion_isr = deduccion_isr / tpagos

                                # tipos_isr = ImpuestoSobreRenta.objects.filter(empresa_reg=suc.empresa, desde__lte=sbb, hasta__gte=sbb, active=True).order_by('-id')
                                # if tipos_isr.count() > 0:
                                #     o_tipoisr = tipos_isr[0]
                                #     deduccion_tipo = TipoDeduccion.objects.filter(tipo_deduccion='ISR', empresa_reg=suc.empresa, active=True)
                                #     if deduccion_tipo.count() > 0:
                                #         orden = int(deduccion_tipo[0].orden)
                                #     else:
                                #         orden = 0
                                #     deduccion_isr = sbb * (float(o_tipoisr.porcentaje) / 100)
                                # #if deduccion_isr > 0:
                                #     tipo_deduccion = {'nombre': 'ISR', 'valor': deduccion_isr, 'orden': orden}
                                #     tipos_deducciones.append(tipo_deduccion)

                                # #if o_planilla.imv:
                                #     dedaplicada = EmpleadoDeducciones.objects.filter(empleado=item, empresa_reg=suc.empresa, deduccion='IMV', active=True)
                                #     if dedaplicada.count() > 0:
                                #         sbb = float(salario_mensual) + float(tigi) + float(tigg) + float(tigp)
                                #         sbb = float(Decimal(sbb).quantize(TWOPLACES))
                                #         tipos_vec = ImpuestoVecinal.objects.filter(empresa_reg=suc.empresa, desde__lte=sbb, hasta__gte=sbb, active=True).order_by('-id')
                                #         if tipos_vec.count() > 0:
                                #             o_tipovec = tipos_vec[0]
                                #             deduccion_tipo = TipoDeduccion.objects.filter(tipo_deduccion='IMV', empresa_reg=suc.empresa, active=True)
                                #             if deduccion_tipo.count() > 0:
                                #                 orden = int(deduccion_tipo[0].orden)
                                #             else:
                                #                 orden = 0

                                #             print(sbb)
                                #             deduccion_vec = sbb * (float(o_tipovec.porcentaje) / 100)
                                #             tpagos = int(30 / item.salaryUnits.dias_salario)
                                #             tpagos = tpagos * 12

                                #             deduccion_vec = deduccion_vec / tpagos
                                #             if deduccion_vec > 0:
                                #                 tipo_deduccion = {'nombre': 'IMV', 'valor': deduccion_vec, 'orden': orden}
                                #                 tipos_deducciones.append(tipo_deduccion)
                                #             print("IMV: " + str(tipos_deducciones))

                                # Deduccion Individual Detalle
                                # deducciones_individuales = DeduccionIndividualDetalle.objects.filter(empleado=item, fecha_valida__gte=o_planilla.fecha_inicio, fecha_valida__lte=o_planilla.fecha_fin, active=True)
                                # #deducciones_individuales = DeduccionIndividualDetalle.objects.filter(empleado=item, fecha_valida__gte=o_planilla.fecha_inicio, active=True)
                                # for item6 in deducciones_individuales:
                                #     sumaControl = 0
                                #     tipo_deduccion = {'nombre': item6.deduccion.deduccion_i, 'valor': item6.valor, 'orden': item6.deduccion.tipo_deduccion.orden}

                                #     tot_ind_ded = tot_ind_ded + item6.valor
                                #     if item6.deduccion.control_saldo:
                                #         if DeduccionIndividualSubDetalle.objects.filter(deducciondetalle=item6).exists():
                                #             o_deduccionsub = DeduccionIndividualSubDetalle.objects.filter(deducciondetalle=item6)[:1]
                                #             o_deduccionsub = o_deduccionsub[0]
                                #             sumaControl = ControlPagosDeduccionIndividual.objects.filter(deduccion=item6).aggregate(Sum('valor'))
                                #             if sumaControl["valor__sum"] != None:
                                #                 if float(sumaControl["valor__sum"]) + float(item6.valor) <= o_deduccionsub.monto:
                                #                     o_control = ControlPagosDeduccionIndividual(
                                #                         planilla = o_planilla,
                                #                         deduccion = item6,
                                #                         valor = float(sumaControl["valor__sum"]) + float(item6.valor)
                                #                     )
                                #                     o_control.save()
                                #             else:
                                #                 if item6.valor <= o_deduccionsub.monto:
                                #                     o_control = ControlPagosDeduccionIndividual(
                                #                         planilla = o_planilla,
                                #                         deduccion = item6,
                                #                         valor = float(item6.valor)
                                #                     )
                                #                     o_control.save()

                                #             tipo_deduccion["deduccion"] = item6.pk

                                #     tipos_deducciones.append(tipo_deduccion)

                                # Deduccion general
                                # deducciones_generales = DeduccionGeneralDetalle.objects.filter(nomina=o_planilla, tipo_pago=o_planilla.frecuencia_pago, tipo_contrato=item.tipo_contrato, fecha_valido__gte=o_planilla.fecha_inicio, fecha_valido__lte=o_planilla.fecha_fin, active=True)
                                # #deducciones_generales = DeduccionGeneralDetalle.objects.filter(nomina=o_planilla, tipo_pago=o_planilla.frecuencia_pago, tipo_contrato=item.tipo_contrato, fecha_valido__gte=o_planilla.fecha_inicio, active=True)
                                # for item7 in deducciones_generales:
                                #     tipo_deduccion = {'nombre': item7.deduccion.deduccion_g, 'valor': item7.valor, 'orden': item7.deduccion.tipo_deduccion.orden}
                                #     tipos_deducciones.append(tipo_deduccion)
                                #     tot_gen_ded = tot_gen_ded + item7.valor

                                # Deducción Individual Planilla
                                # #deducciones_planilla = DeduccionIndividualPlanilla.objects.filter(empleado=item, planilla=o_planilla, active=True)
                                # for item8 in deducciones_planilla:
                                #     tipo_deduccion = {'nombre': item8.deduccion.deduccion_i, 'valor': item8.valor, 'orden': item8.deduccion.tipo_deduccion.orden}
                                #     tipos_deducciones.append(tipo_deduccion)
                                #     tot_pla_ded = tot_pla_ded + item8.valor

                                d_deducciones = DeduccionEmpleado.objects.filter(empleado=item, planilla=o_planilla, active=True)
                                for d_deduccion in d_deducciones:
                                    tot_deducciones += d_deduccion.monto
                                    GuardarDetalleDeduccion(
                                        item,
                                        o_planilla,
                                        d_deduccion.deduccion.deduccion_tipo,
                                        d_deduccion.deduccion,
                                        d_deduccion.monto,
                                        d_deduccion,
                                        suc.empresa,
                                        suc,
                                        request.user,
                                    )

                                # #lista_deducciones_tipos = TipoDeduccion.objects.filter(empresa_reg=suc.empresa, active=True).order_by('orden')
                                # for item9 in lista_deducciones_tipos:
                                #     for item9_1 in tipos_deducciones:
                                #         hay_deduccion = False
                                #         id_dedu = 0

                                #         if float(item9_1["orden"]) == float(item9.orden):

                                #             total_ingreso = total_ingreso - float(item9_1["valor"])
                                #             total_egreso = total_egreso + float(item9_1["valor"])
                                #             if "deduccion" in item9_1:
                                #                 hay_deduccion = True
                                #                 id_dedu = item9_1["deduccion"]
                                #             GuardarDetalleDeduccionIngreso(2, item9_1["nombre"], item9_1["valor"], item, o_planilla, suc.empresa, suc, request.user, item9, hay_deduccion, id_dedu)

                                # total_egreso = float(total_egreso) + float(tot_ind_ded)
                                # total_ingreso = float(total_ingreso) - float(tot_ind_ded)
                                total_ingreso = (total_ingreso - (dias_ausencia_sin_pago * salario_diario) + float(tot_ingreso))
                                if o_planilla.especial:
                                    valor_sueldo = 0

                                o_planilla_detalle = PlanillaDetalle(
                                    planilla=o_planilla,
                                    empleado=item,
                                    salario_diario=salario_diario,
                                    dias_salario=item.salaryUnits.dias_salario,
                                    dias_ausentes_sin_pago=dias_ausencia_sin_pago,
                                    dias_ausentes_con_pago=dias_ausencia_con_pago,
                                    total_ingresos=valor_sueldo + tot_pla_ing,
                                    total_deducciones=float(total_egreso) + float(tot_deducciones),
                                    comentario=comentario,
                                    empresa_reg=suc.empresa,
                                    sucursal_reg=suc,
                                    user_reg=request.user,
                                    active=True,
                                )
                                o_planilla_detalle.save()

                                o_tipo_ing_sal = None
                                if IngresoTipo.objects.filter(ingreso_tipo="Salario", empresa_reg=suc.empresa, active=True).exists():
                                    o_tipo_ing_sal = IngresoTipo.objects.get(ingreso_tipo="Salario", empresa_reg=suc.empresa, active=True)

                                o_planilla_detalle_ingreso = PlanillaDetalleIngresos(
                                    empleado=item,
                                    planilla=o_planilla,
                                    ingreso="Salario ",
                                    # valor = total_ingreso,
                                    tipo_ingreso=o_tipo_ing_sal,
                                    valor=valor_sueldo,
                                    empresa_reg=suc.empresa,
                                    sucursal_reg=suc,
                                    user_reg=request.user,
                                )
                                o_planilla_detalle_ingreso.save()

                            data = {"error": False, "mensaje": "Exito!."}
                            return JsonResponse(data)
                        else:
                            data = {
                                "error": False,
                                "mensaje": "No existe registro de planilla!.",
                            }
                            return JsonResponse(data)
                    else:
                        data = {
                            "error": True,
                            "mensaje": "Tipo de Dato como parámetro no es válido.",
                        }
                        return JsonResponse(data)
            else:
                data = {"error": True, "mensaje": "El método no es válido."}
                return JsonResponse(data)
        else:
            data = {"error": True, "mensaje": "No es una petición asíncrona."}
            return JsonResponse(data)
    except ValueError as mensaje:
        data = {"error": True, "mensaje": mensaje}
        return JsonResponse(data)


def GuardarDetalleDeduccionIngreso(tipo, mensaje, valor, empleado, planilla, empresa, sucursal, usuario, tipo_registro,hay_deduccion, id_dedu):
    tipo_reg = None
    o_deduded = None
    if tipo_registro:
        tipo_reg = tipo_registro

    if tipo == 1:
        o_ingreso = PlanillaDetalleIngresos(
            empleado=empleado,
            planilla=planilla,
            ingreso=mensaje,
            tipo_ingreso=tipo_reg,
            valor=valor,
            empresa_reg=empresa,
            sucursal_reg=sucursal,
            user_reg=usuario,
        )
        o_ingreso.save()
    elif tipo == 2:
        if DeduccionEmpleado.objects.filter(pk=id_dedu).exists():
            o_deduded = DeduccionEmpleado.objects.get(pk=id_dedu)
        o_deduccion = PlanillaDetalleDeducciones(
            empleado=empleado,
            planilla=planilla,
            deduccion=mensaje,
            deduccion_f = o_deduded,
            tipo_deduccion=tipo_reg,
            valor=valor,
            empresa_reg=empresa,
            sucursal_reg=sucursal,
            user_reg=usuario,
        )
        o_deduccion.save()
        # if DeduccionIndividualDetalle.objects.filter(pk=id_dedu).exists():
        #     o_deduded = DeduccionEmpleado.objects.get(pk=id_dedu)
        #     o_reg = DetallePlanillaDetalleDeduccion(
        #         planilla_detalle_ded=o_deduccion, deduccion_detalle=o_deduded
        #     )
        #     o_reg.save()


def GuardarDetalleIngreso(empleado, planilla, ingreso, tipo_ingreso, valor, empresa, sucursal_reg, user_reg):
    o_ingreso = PlanillaDetalleIngresos(
        empleado=empleado,
        planilla=planilla,
        ingreso=ingreso,
        tipo_ingreso=tipo_ingreso,
        valor=valor,
        empresa_reg=empresa,
        sucursal_reg=sucursal_reg,
        user_reg=user_reg,
    )
    o_ingreso.save()

def GuardarDetalleDeduccion(empleado, planilla, deduccion, tipo_deduccion, valor, deduccion_f, empresa_reg, sucursal_reg, user_reg):
    o_deduccion = PlanillaDetalleDeducciones(
        empleado=empleado,
        planilla=planilla,
        deduccion=deduccion,
        deduccion_f=deduccion_f,
        tipo_deduccion=tipo_deduccion,
        valor=valor,
        empresa_reg=empresa_reg,
        sucursal_reg=sucursal_reg,
        user_reg=user_reg,
        )
    o_deduccion.save()

def planilla_calculos_empleado(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                total_dias = 0
                dias_ausencia_con_pago = 0
                dias_ausencia_sin_pago = 0
                tot_ded_ind = 0
                tot_ind_ded = 0
                tot_ind_ing = 0
                tot_gen_ing = 0
                tot_gen_ded = 0
                tot_pla_ing = 0
                tot_pla_ded = 0
                empleado_id = request.POST["empleado_id"]
                planilla_id = request.POST["planilla_id"]
                o_empleado = Employee.objects.get(pk=empleado_id)
                o_planilla = Planilla.objects.get(pk=planilla_id)
                suc = Branch.objects.get(pk=request.session["sucursal"])

                salario_mes = float(o_empleado.salario_diario) * 30

                ausencias_con_pago = Ausentismo.objects.filter(
                    empleado=o_empleado,
                    sucursal_reg=suc,
                    motivo__pagado=True,
                    desde__gte=o_planilla.fecha_inicio,
                    desde__lte=o_planilla.fecha_fin,
                    hasta__gte=o_planilla.fecha_inicio,
                    hasta__lte=o_planilla.fecha_fin,
                )
                if ausencias_con_pago.count() > 0:
                    dias_ausencia_con_pago = 1
                    for item in ausencias_con_pago:
                        dias_ausencia_con_pago = (
                            dias_ausencia_con_pago + (item.hasta - item.desde).days
                        )

                ausencias_sin_pago = Ausentismo.objects.filter(
                    empleado=o_empleado,
                    sucursal_reg=suc,
                    motivo__pagado=False,
                    desde__gte=o_planilla.fecha_inicio,
                    desde__lte=o_planilla.fecha_fin,
                    hasta__gte=o_planilla.fecha_inicio,
                    hasta__lte=o_planilla.fecha_fin,
                )
                if ausencias_sin_pago.count() > 0:
                    dias_ausencia_sin_pago = 1
                    for item in ausencias_sin_pago:
                        dias_ausencia_sin_pago = (
                            dias_ausencia_sin_pago + (item.hasta - item.desde).days
                        )
                # Deduccion Individual Detalle
                deducciones_individuales = DeduccionIndividualDetalle.objects.filter(
                    empleado=o_empleado,
                    fecha_valida__gte=o_planilla.fecha_inicio,
                    fecha_valida__lte=o_planilla.fecha_fin,
                    active=True,
                )
                for item in deducciones_individuales:
                    tot_ind_ded = tot_ind_ded + item.valor

                # Ingreso Individual Detalle
                ingresos_individuales = IngresoIndividualDetalle.objects.filter(
                    empleado=o_empleado,
                    fecha_valida__gte=o_planilla.fecha_inicio,
                    fecha_valida__lte=o_planilla.fecha_fin,
                    active=True,
                )
                for item in ingresos_individuales:
                    tot_ind_ing = tot_ind_ing + item.valor

                # Ingreso general
                ingresos_generales = IngresoGeneralDetalle.objects.filter(
                    nomina=o_planilla,
                    tipo_pago=o_planilla.frecuencia_pago,
                    tipo_contrato=o_empleado.tipo_contrato,
                    fecha_valida__gte=o_planilla.fecha_inicio,
                    fecha_valida__lte=o_planilla.fecha_fin,
                    active=True,
                )
                for item in ingresos_generales:
                    tot_gen_ing = tot_gen_ing + item.valor

                # Deduccion general
                deducciones_generales = DeduccionGeneralDetalle.objects.filter(
                    nomina=o_planilla,
                    tipo_pago=o_planilla.frecuencia_pago,
                    tipo_contrato=o_empleado.tipo_contrato,
                    fecha_valido__gte=o_planilla.fecha_inicio,
                    fecha_valido__lte=o_planilla.fecha_fin,
                    active=True,
                )
                for item in deducciones_generales:
                    tot_gen_ded = tot_gen_ded + item.valor

                # Ingreso Individual Planilla
                ingresos_planilla = IngresoIndividualPlanilla.objects.filter(
                    empleado=o_empleado, planilla=o_planilla, active=True
                )
                for item in ingresos_planilla:
                    tot_pla_ing = tot_pla_ing + item.valor

                # Deducción Individual Planilla
                deducciones_planilla = DeduccionIndividualPlanilla.objects.filter(
                    empleado=o_empleado, planilla=o_planilla, active=True
                )
                for item in deducciones_planilla:
                    tot_pla_ded = tot_pla_ded + item.valor

                # Deducciones de ley
                deduccion_ihss = 0
                tipos_ihss = SeguroSocial.objects.filter(active=True)
                for item in tipos_ihss:
                    if salario_mes > float(item.techo):
                        salario_mes = float(item.techo)
                    deduccion_ihss = deduccion_ihss + (
                        salario_mes * (float(item.porcentaje_e) / 100)
                    )

                deduccion_isr = 0
                tipo_isr = ImpuestoSobreRenta.objects.filter(
                    desde__lte=float(o_empleado.salary) * 12,
                    hasta__gte=float(o_empleado.salary) * 12,
                )

                #     deduccion_isr = salario_mes *  (float(tipo_isr[0].porcentaje) / 100)
                # else:
                #     deduccion_isr = 0

                detalles_planillas = PlanillaDetalle.objects.filter(
                    planilla=o_planilla, empleado=o_empleado
                )
                if detalles_planillas.count() > 0:
                    detalles_planillas.delete()

                o_planilladetalle = PlanillaDetalle(
                    planilla=o_planilla,
                    empleado=o_empleado,
                    salario_diario=o_empleado.salario_diario,
                    dias_salario=o_planilla.frecuencia_pago.dias_salario,
                    dias_ausentes_sin_pago=dias_ausencia_sin_pago,
                    dias_ausentes_con_pago=dias_ausencia_con_pago,
                    total_deducciones=tot_ind_ded
                    + tot_gen_ded
                    + tot_pla_ded
                    + deduccion_ihss,
                    total_ingresos=tot_ind_ing + tot_gen_ing + tot_pla_ing,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    active=True,
                    user_reg=request.user,
                )
                o_planilladetalle.save()
                detalles_planillas_deducciones = (
                    PlanillaDetalleDeducciones.objects.filter(planilla=o_planilla)
                )
                if detalles_planillas_deducciones.count() > 0:
                    detalles_planillas_deducciones.delete()

                for item in deducciones_generales:
                    o_pladetded = PlanillaDetalleDeducciones(
                        empleado=o_empleado,
                        planilla=o_planilla,
                        deduccion=item.deduccion.deduccion_g,
                        valor=item.valor,
                        empresa_reg=suc.empresa,
                        sucursal_reg=suc,
                        user_reg=request.user,
                    )
                    o_pladetded.save()

                for item in deducciones_individuales:
                    o_pladetded = PlanillaDetalleDeducciones(
                        empleado=o_empleado,
                        planilla=o_planilla,
                        deduccion=item.deduccion.deduccion_i,
                        valor=item.valor,
                        empresa_reg=suc.empresa,
                        sucursal_reg=suc,
                        user_reg=request.user,
                    )
                    o_pladetded.save()

                for item in deducciones_planilla:
                    o_pladetded = PlanillaDetalleDeducciones(
                        empleado=o_empleado,
                        planilla=o_planilla,
                        deduccion=item.deduccion.deduccion_i,
                        valor=item.valor,
                        empresa_reg=suc.empresa,
                        sucursal_reg=suc,
                        user_reg=request.user,
                    )
                    o_pladetded.save()

                regs_planilla_ingresos = PlanillaDetalleIngresos.objects.filter(
                    planilla=o_planilla
                )
                if regs_planilla_ingresos.count() > 0:
                    regs_planilla_ingresos.delete()

                for item in ingresos_generales:
                    o_ing = PlanillaDetalleIngresos(
                        empleado=o_empleado,
                        planilla=o_planilla,
                        ingreso=item.ingreso.ingreso_g,
                        valor=item.valor,
                        empresa_reg=suc.empresa,
                        sucursal_reg=suc,
                        user_reg=request.user,
                    )
                    o_ing.save()

                for item in ingresos_individuales:
                    o_ing = PlanillaDetalleIngresos(
                        empleado=o_empleado,
                        planilla=o_planilla,
                        ingreso=item.ingreso.ingreso_i,
                        valor=item.valor,
                        empresa_reg=suc.empresa,
                        sucursal_reg=suc,
                        user_reg=request.user,
                    )
                    o_ing.save()

                for item in ingresos_planilla:
                    o_ing = PlanillaDetalleIngresos(
                        empleado=o_empleado,
                        planilla=o_planilla,
                        ingreso=item.ingreso.ingreso_i,
                        valor=item.valor,
                        empresa_reg=suc.empresa,
                        sucursal_reg=suc,
                        user_reg=request.user,
                    )
                    o_ing.save()

                o_pladetded = PlanillaDetalleDeducciones(
                    empleado=o_empleado,
                    planilla=o_planilla,
                    deduccion="I.H.S.S.",
                    valor=deduccion_ihss,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    user_reg=request.user,
                )
                o_pladetded.save()

                o_pladetded = PlanillaDetalleDeducciones(
                    empleado=o_empleado,
                    planilla=o_planilla,
                    deduccion="I.S.R.",
                    valor=deduccion_isr,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    user_reg=request.user,
                )
                o_pladetded.save()

                data = {
                    "error": False,
                    "mensaje": "El proceso ha finalizado.",
                }
            else:
                data = {
                    "error": True,
                    "mensaje": "El método no está permitido.",
                }
        else:
            data = {
                "error": True,
                "mensaje": "La solicitud no es asíncrona.",
            }
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": str(ex),
        }
    return JsonResponse(data)

def planilla_cerrar(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                registro_id = request.POST["id"]
                if len(registro_id) > 0:
                    registro_id = int(registro_id)
                    if registro_id > 0:
                        o_planilla = Planilla.objects.get(pk=registro_id)
                        if o_planilla:
                            Planilla.objects.filter(pk=registro_id).update(cerrada=True)
                            data = {
                                "error": False,
                                "mensaje": "Se ha cerrado la planilla",
                            }
                            return JsonResponse(data)
                        else:
                            data = {
                                "error": True,
                                "mensaje": "No existe registro",
                            }
                            return JsonResponse(data)
                    else:
                        data = {
                            "error": True,
                            "mensaje": "No se ha pasado un valor válido como parámetro",
                        }
                        return JsonResponse(data)
                else:
                    data = {
                        "error": True,
                        "mensaje": "El método no está permitido",
                    }
                    return JsonResponse(data)
            else:
                data = {
                    "error": True,
                    "mensaje": "El método no está permitido",
                }
                return JsonResponse(data)
        else:
            data = {
                "error": True,
                "mensaje": "El tipo de petición http no es válida",
            }
            return JsonResponse(data)
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": str(ex),
        }
        return JsonResponse(data)

@login_required(login_url="/form/iniciar-sesion/")
def planilla_reporte_general(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    planillas = Planilla.objects.filter(sucursal_reg=suc, active=True, cerrada=True)
    departamentos = Department.objects.filter(empresa_reg=suc.empresa, active=True)
    tipos_contrato = TipoContrato.objects.filter(empresa_reg=suc.empresa, active=True)
    tipos_nomina = TipoNomina.objects.filter(empresa_reg=suc.empresa, active=True)
    frecuencia_pagos = SalaryUnit.objects.filter(empresa_reg=suc.empresa, active=True)
    sucursales = Branch.objects.filter(empresa=suc.empresa, active=True)
    return render(request, "planilla-reporte-general.html", { "planillas": planillas, "departamentos": departamentos, "tipos_contratos": tipos_contrato, "tipos_planillas": tipos_nomina, "frecuencias_pagos": frecuencia_pagos, 'sucursales':sucursales})

def generar_reporte_general(request):
    verificaSucursal(request)
    registro_id = None
    o_tipo_contrato = None
    o_tipo_planilla = None
    o_departamento = None
    o_frecuencia_pago = None
    desde = None
    hasta = None
    cerrada = True
    q_list = []
    columnas = []
    detalle = []
    detalles = []
    datos_planilla = []
    mensaje = "No hay datos"
    data = {"error": False, "mensaje": mensaje}
    verificaSucursal(request)

    departamento_id = request.GET.get("cboDepartamento")
    tipo_contrato_id = request.GET.get("cboTipoContrato")
    tipo_planilla_id = request.GET.get("cboTipoPlanilla")
    frecuencia_pago_id = request.GET.get("cboFrecuenciaPago")
    estado_contrato = request.GET.get("cboEstadoContrato")
    desde = request.GET.get("txtDesde")
    hasta = request.GET.get("txtHasta")
    suc = Branch.objects.get(pk=request.session["sucursal"])

    if len(desde) == 0:
        data = {"error": True, "mensaje": "Seleccione un rango de fecha válido"}
        return render(request, "reportes/reporte-planilla-general.html", data)

    if len(hasta) == 0:
        data = {"error": True, "mensaje": "Seleccione un rango de fecha válido"}
        return render(request, "reportes/reporte-planilla-general.html", data)

    desde = datetime.datetime.strptime(desde, "%d/%m/%Y").date()
    hasta = datetime.datetime.strptime(hasta, "%d/%m/%Y").date()
    if estado_contrato == "2":
        q_list.append(Q(planilla__cerrada=True))
    elif estado_contrato == "1":
        q_list.append(Q(planilla__cerrada=False))
    q_list.append(Q(planilla__fecha_inicio__gte=desde, planilla__fecha_fin__lte=hasta))
    if int(departamento_id) > 0:
        tot_reg = Department.objects.filter(pk=departamento_id).count()
        if tot_reg > 0:
            o_departamento = Department.objects.get(pk=departamento_id)
            if o_departamento:
                q_list.append(Q(empleado__dept=o_departamento))

    if int(tipo_contrato_id) > 0:
        tot_reg = TipoContrato.objects.filter(pk=tipo_contrato_id).count()
        if tot_reg > 0:
            o_tipo_contrato = TipoContrato.objects.filter(pk=tipo_contrato_id)
            if o_tipo_contrato:
                q_list.append(Q(empleado__tipo_contrato=o_tipo_contrato))

    if int(tipo_planilla_id) > 0:
        tot_reg = TipoNomina.objects.filter(pk=tipo_planilla_id).count()
        if tot_reg > 0:
            o_tipo_planilla = TipoNomina.objects.get(pk=tipo_planilla_id)
            if o_tipo_planilla:
                q_list.append(Q(empleado__tipo_nomina=o_tipo_planilla))

    if int(frecuencia_pago_id) > 0:
        tot_reg = SalaryUnit.objects.filter(pk=frecuencia_pago_id).count()
        if tot_reg > 0:
            o_frecuencia_pago = SalaryUnit.objects.get(pk=frecuencia_pago_id)
            if o_frecuencia_pago:
                q_list.append(Q(empleado__salaryUnits=o_frecuencia_pago))

    if len(q_list) == 0:
        data = {"error": True, "mensaje": "No hay datos"}
        return JsonResponse(data)
    else:
        val_list_ing = (
            PlanillaDetalleIngresos.objects.filter(
                functools.reduce(operator.and_, q_list)
            )
            .values_list("empleado__id", flat=True)
            .distinct()
        )
        val_list_ded = (
            PlanillaDetalleDeducciones.objects.filter(
                functools.reduce(operator.and_, q_list)
            )
            .values_list("empleado__id", flat=True)
            .distinct()
        )
        empleados = Employee.objects.filter(pk__in=val_list_ing)

        columnas = [{"title": "Codigo"}, {"title": "Nombre"}, {"title": "Departamento"}]
        grupos_flat = (
            PlanillaDetalleIngresos.objects.filter(
                Q(planilla__fecha_inicio__gte=desde, planilla__fecha_fin__lte=hasta)
            )
            .exclude(tipo_ingreso=None)
            .values_list("tipo_ingreso__ingreso_tipo", flat=True)
            .order_by("tipo_ingreso__indice_relevancia")
            .distinct()
        )
        grupos_flat_ded = PlanillaDetalleDeducciones.objects.filter(Q(planilla__fecha_inicio__gte=desde, planilla__fecha_fin__lte=hasta)).exclude(tipo_deduccion=None).values_list("tipo_deduccion__deduccion_tipo", flat=True).order_by("tipo_deduccion__indice_relevancia").distinct()
        # grupos_flat = list(set(grupos_flat))
        # grupos_flat_ded = list(set(grupos_flat_ded))
        for empleado in empleados:
            detallesfila = []
            total_ingreso = 0
            total_deducciones = 0
            salario = 0
            q_list2 = []

            datos_empleado = {}
            datos_empleado2 = []
            Nombre = ""
            Nombre = empleado.firstName
            if empleado.middleName:
                Nombre = Nombre + " " + empleado.middleName
            Nombre = Nombre + " " + empleado.lastName
            datos_empleado["Empleado_Id"] = empleado.extEmpNo
            datos_empleado["Nombre"] = Nombre
            if empleado.dept:
                datos_empleado["Departamento"] = empleado.dept.description
            else:
                datos_empleado["Departamento"] = ""
            # datos_empleado['Sueldo'] = 0

            # o_pla_ing = PlanillaDetalleIngresos.objects.filter(Q(planilla__fecha_inicio__gte=desde, planilla__fecha_fin__lte=hasta, empleado=empleado))
            # for detalle1 in o_pla_ing:
            #     if not datos_empleado['Fecha pago']:
            #         datos_empleado['Fecha pago'] = detalle1.planilla.fecha_pago.strftime("%d/%m/%Y")

            # if empleado == detalle1.empleado and detalle1.ingreso.count("SALARIO") > 0 and not detalle1.tipo_ingreso:
            #     datos_empleado['Sueldo'] = formato_millar(detalle1.valor)
            #     total_ingreso = detalle1.valor

            for grupo in grupos_flat:

                tot_col = 0
                for columna in columnas:
                    if columna["title"] == grupo:
                        tot_col += 1
                if tot_col == 0:
                    columnas.append({"title": grupo})
                    datos_empleado[grupo] = formato_millar(0)

                if not grupo in datos_empleado:
                    datos_empleado[grupo] = formato_millar(0)

                o_pla_ing = PlanillaDetalleIngresos.objects.filter(
                    Q(
                        planilla__fecha_inicio__gte=desde,
                        empleado=empleado,
                        planilla__fecha_fin__lte=hasta,
                        tipo_ingreso__grupo=grupo,
                    )
                ).order_by("tipo_ingreso__orden", "ingreso")
                for detalle in o_pla_ing:
                    if detalle.tipo_ingreso:
                        if (
                            detalle.tipo_ingreso.grupo == grupo
                            and detalle.empleado == empleado
                        ):
                            datos_empleado[grupo] = formato_millar(
                                float(datos_empleado[grupo].replace(",", ""))
                                + float(detalle.valor)
                            )
                            total_ingreso += detalle.valor
                        else:
                            datos_empleado[grupo] = formato_millar(
                                float(datos_empleado[grupo].replace(",", "")) + 0
                            )

            datos_empleado["Total Ingresos"] = formato_millar(total_ingreso)
            tot_col = 0
            for columna in columnas:
                if columna["title"] == "Total Ingreso":
                    tot_col += 1
            if tot_col == 0:
                columnas.append({"title": "Total Ingreso"})

            for grupo in grupos_flat_ded:
                tot_col = 0
                for columna in columnas:
                    if columna["title"] == grupo:
                        tot_col += 1
                if tot_col == 0:
                    columnas.append({"title": grupo})
                    datos_empleado[grupo] = formato_millar(0)

                if not grupo in datos_empleado:
                    datos_empleado[grupo] = formato_millar(0)

                o_pla_ded = PlanillaDetalleDeducciones.objects.filter(
                    Q(
                        planilla__fecha_inicio__gte=desde,
                        planilla__fecha_fin__lte=hasta,
                        tipo_deduccion__grupo=grupo,
                        empleado=empleado,
                    )
                ).order_by("tipo_deduccion__orden", "deduccion")

                for detalle in o_pla_ded:
                    if detalle.tipo_deduccion:
                        if (
                            detalle.tipo_deduccion.grupo == grupo
                            and detalle.empleado == empleado
                        ):
                            datos_empleado[grupo] = formato_millar(
                                float(datos_empleado[grupo].replace(",", ""))
                                + float(detalle.valor)
                            )
                            total_deducciones += detalle.valor
                        else:
                            datos_empleado[grupo] = formato_millar(
                                float(datos_empleado[grupo].replace(",", "")) + 0
                            )

            datos_empleado["Total Deducciones"] = formato_millar(total_deducciones)
            datos_planilla.append(datos_empleado)
            datos_empleado["Total Neto"] = formato_millar(
                total_ingreso - total_deducciones
            )
        filas_detalles = []

        for elemento in datos_planilla:
            filas_detalles.append(list(elemento.values()))

        columnas.append({"title": "Total Deducciones"})
        columnas.append({"title": "Total Devengado"})
        data = {
            "error": False,
            "mensaje": "Se han encontrado datos.",
            "data": filas_detalles,
            "columns": columnas,
        }
        # return JsonResponse(data)

    if len(departamento_id) > 0:
        pass
    else:
        data = {"error": True, "mensaje": "No se pasó un valor válido como parámetro."}
    return render(request, "reportes/reporte-planilla-general.html", data)

def planilla_ver_registro(request):
    error = False
    mensaje = ""
    titulo = ""
    dato = None
    id = 0
    if request.is_ajax():
        id = request.GET.get("id")
        if id == 0:
            error = True
            mensaje = "El registro no existe."
        else:
            tot_reg = Planilla.objects.filter(pk=id).count()
            if tot_reg > 0:
                dato = Planilla.objects.get(pk=id)
                error = False
            else:
                error = True
                mensaje = "No existe el registro."
    else:
        error = True
        mensaje = "El método no está permitido."

    if error:
        titulo = "Error - Mensaje"
    else:
        titulo = "Ver registro"
    return render(
        request,
        "ajax/planilla-modal.html",
        {"error": error, "mensaje": mensaje, "titulo": titulo, "dato": dato},
    )

def planilla_obtener_ver_empleado(request):
    try:
        mensaje = ""
        codigos = {}
        datos2 = []
        datos3 = []
        total_salario = 0
        suma_total_ingresos = 0
        suma_total_deducciones = 0
        total_neto = 0
        l_empleados = []
        detalles = False
        if request.is_ajax():
            empleado_id = request.GET.get("empleado_id")
            planilla_id = request.GET.get("planilla_id")
            empleado_id = int(empleado_id)
            planilla_id = int(planilla_id)
            planilla = Planilla.objects.get(pk=planilla_id)
            empleado = Employee.objects.get(pk=empleado_id)
            ingresos = PlanillaDetalleIngresos.objects.filter(
                planilla=planilla, empleado=empleado
            ).order_by("tipo_ingreso__indice_relevancia")
            for item1 in ingresos:
                objeto1 = {
                    "id": item1.pk,
                    "empleado": item1.empleado,
                    "planilla": item1.planilla,
                    "ingreso": item1.ingreso,
                    "valor": locale.format("%.2f", item1.valor, grouping=True),
                }
                suma_total_ingresos += float(item1.valor)
                datos2.append(objeto1)

            deducciones = PlanillaDetalleDeducciones.objects.filter(planilla=planilla, empleado=empleado).order_by("tipo_deduccion__indice_relevancia")
            print(deducciones)
            for item2 in deducciones:
                if item2.deduccion_f:
                    if item2.deduccion_f.detalle:
                        detalles = False
                        if DeduccionIndividualSubDetalle.objects.filter(deduccion=item2.deduccion_f).exists():
                            detalles = True
            #     tiene_sub = False
            #     tipo_ded = DeduccionTipo.objects.get(pk=item2["tipo_deduccion"])
            #     var1_flat = PlanillaDetalleDeducciones.objects.filter(
            #         planilla=planilla, empleado=empleado, tipo_deduccion=tipo_ded
            #     ).values_list("pk", flat=True)
            #     var2_flat = DetallePlanillaDetalleDeduccion.objects.filter(
            #         planilla_detalle_ded__in=var1_flat
            #     ).values_list("deduccion_detalle", flat=True)
            #     if DeduccionIndividualSubDetalle.objects.filter(
            #         deducciondetalle__in=var2_flat
            #     ).exists():
            #         tiene_sub = True
                objeto2 = {
                    "planilla": item2.planilla,
                    "deduccion": item2.deduccion,
                    "deduccion_f": item2.deduccion_f,
                    "valor": locale.format("%.2f", item2.valor, grouping=True),
                    "empleado": item2.empleado,
                    "detalles": detalles,
                }
                datos3.append(objeto2)
                suma_total_deducciones += float(item2.valor)
            
            total_neto = suma_total_ingresos - suma_total_deducciones
            total_neto = locale.format("%.2f", total_neto, grouping=True)
            # suma_total_ingresos = locale.format(
            #     "%.2f", suma_total_ingresos, grouping=True
            # )
            # suma_total_deducciones = locale.format(
            #     "%.2f", suma_total_deducciones, grouping=True
            # )
            error = False
            mensaje = "¡El proceso se ha completado con éxito!"
            data = {
                "error": error,
                "mensaje": mensaje,
                "ingresos": datos2,
                "deducciones": datos3,
                "subingresos": formato_millar(suma_total_ingresos),
                "subdeducciones": formato_millar(suma_total_deducciones),
                "total_neto": total_neto,
            }
            
        else:
            error = True
            mensaje = "El método no está permitido."
            data = {"error": error, "mensaje": mensaje}
        
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": str(ex),
        }
        print(str(ex))
    return render(request, "ajax/ver-planilla-empleado.html", data)

def planilla_obtener_subdetalle_deduccion(request):
    data = {"error": True, "msj": "No se realizó la operación"}
    planilla = None
    deduccion_tipo = None
    if request.is_ajax():
        deduccion_id = request.GET.get("deduccion_id")
        planilla_id = request.GET.get("planilla_id")
        empleado_id = request.GET.get("empleado_id")
        if Planilla.objects.filter(pk=planilla_id).exists():
            planilla = Planilla.objects.get(pk=planilla_id)
            if DeduccionEmpleado.objects.filter(pk=deduccion_id).exists():
                # tipo_deduccion = TipoDeduccion.objects.get(pk=deduccion_id)
                if Employee.objects.filter(pk=empleado_id).exists():
                    datos = []
                    empleado = Employee.objects.get(pk=empleado_id)
                    # lista_detal = ControlPagosDeduccionIndividual.objects.filter(planilla=planilla, deduccion__deduccion__tipo_deduccion=tipo_deduccion, deduccion__deduccion__empleado=empleado)
                    # lista_control_flat = ControlPagosDeduccionIndividual.objects.filter(
                    #     planilla=planilla,
                    #     deduccion__deduccion__tipo_deduccion=tipo_deduccion,
                    #     deduccion__empleado=empleado,
                    # ).values_list("deduccion_id", flat=True)
                    lista_detal = DeduccionIndividualSubDetalle.objects.filter(
                        deduccion__pk=deduccion_id
                    )
                    for item in lista_detal:
                        o_ldetal = {
                            "descripcion": item.descripcion,
                            "monto_total": item.monto,
                        }
                        datos.append(o_ldetal)
                    data = {
                        "error": False,
                        "msj": "Se han encontrado los datos",
                        "datos": datos,
                    }
                else:
                    data = {
                        "error": True,
                        "msj": "El empleado como parámetro no existe.",
                    }
                    return JsonResponse(data)
            else:
                data = {
                    "error": True,
                    "msj": "El tipo de deducción como parámetro no existe.",
                }
                return JsonResponse(data)
        else:
            data = {"error": True, "msj": "La planilla como parámetro no existe."}
            return JsonResponse(data)
    else:
        pass
    return JsonResponse(data)

def planilla_generada(request):
    datos = []
    datos2 = []
    datos3 = []
    suma_neta = []
    detalle_planilla = None
    ingresos = 0
    deducciones = 0
    suma_total_ingresos = 0
    suma_total_deducciones = 0
    if request.is_ajax():
        planilla_id = int(request.GET.get("Id"))
        if planilla_id == 0:
            error = True
            mensaje = "El registro no existe."
        else:
            detalle_planilla = PlanillaDetalle.objects.filter(planilla__pk=planilla_id).order_by('empleado__firstName')
            for item in detalle_planilla:
                datos2 = []
                datos3 = []
                dias_trabajo = 0
                dias_trabajo = float(item.dias_salario) - float(
                    item.dias_ausentes_sin_pago
                )
                total_salario = float(dias_trabajo) * float(item.salario_diario)
                ingresos = (
                    PlanillaDetalleIngresos.objects.filter(
                        planilla__pk=planilla_id, empleado=item.empleado
                    )
                    .order_by("tipo_ingreso__indice_relevancia")
                    .values("empleado", "planilla", "ingreso")
                    .annotate(Sum("valor"))
                )

                for item1 in ingresos:
                    objeto1 = {
                        "ingreso": item1["ingreso"],
                        "valor": locale.format(
                            "%.2f", item1["valor__sum"], grouping=True
                        ),
                    }
                    datos2.append(objeto1)

                deducciones = (
                    PlanillaDetalleDeducciones.objects.filter(
                        planilla__pk=planilla_id, empleado=item.empleado
                    )
                    .order_by("tipo_deduccion__indice_relevancia")
                    .values("empleado", "planilla", "deduccion")
                    .annotate(Sum("valor"))
                )

                for item2 in deducciones:
                    objeto2 = {
                        "deduccion": item2["deduccion"],
                        "valor": locale.format(
                            "%.2f", item2["valor__sum"], grouping=True
                        ),
                    }
                    datos3.append(objeto2)

                objeto = {
                    "id": item.pk,
                    "empleado": item.empleado,
                    "planilla": item.planilla,
                    "salario_diario": item.salario_diario,
                    "dias_ausentes_sin_pago": item.dias_ausentes_sin_pago,
                    "dias_ausentes_con_pago": item.dias_ausentes_con_pago,
                    "total_ingresos": locale.format(
                        "%.2f", float(item.total_ingresos), grouping=True
                    ),
                    "total_deducciones": locale.format(
                        "%.2f", item.total_deducciones, grouping=True
                    ),
                    "total_salario": locale.format(
                        "%.2f",
                        item.total_ingresos - item.total_deducciones,
                        grouping=True,
                    ),
                    "ingreso_detalle": datos2,
                    "deduccion_detalle": datos3,
                }
                datos.append(objeto)
                suma_total_ingresos += float(item.total_ingresos)
                suma_total_deducciones += float(item.total_deducciones)

            suma_neta = suma_total_ingresos - suma_total_deducciones
            suma_total_ingresos = locale.format(
                "%.2f", suma_total_ingresos, grouping=True
            )
            suma_total_deducciones = locale.format(
                "%.2f", suma_total_deducciones, grouping=True
            )
            suma_neta = locale.format("%.2f", suma_neta, grouping=True)

            error = False
            mensaje = "Datos encontrados"
    else:
        error = True
        mensaje = "Método no permitido"

    return render(
        request,
        "ajax/planilla_empleados_lista.html",
        {
            "detalle_planilla": datos,
            "ingresos": datos2,
            "deducciones": datos3,
            "total_deducciones": suma_total_deducciones,
            "total_ingresos": suma_total_ingresos,
            "total_neto": suma_neta,
        },
    )


# ------------------------------END AJAX---------------------------------

# endregion

# region Código para Seguro Social


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_segurosocial", raise_exception=True)
def segurosocial_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_ingresogeneral"):
        lista = SeguroSocial.objects.filter(empresa_reg=suc.empresa)
    else:
        lista = SeguroSocial.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(request, "segurosocial-listado.html", {"lista": lista})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_segurosocial", raise_exception=True)
def segurosocial_form(request):
    return render(request, "segurosocial-form.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_segurosocial", raise_exception=True)
def segurosocial_editar(request, id):
    dato = SeguroSocial.objects.get(pk=id)
    return render(request, "segurosocial-form.html", {"dato": dato, "editar": True})


# ---------------------AJAX-------------------------------


def segurosocial_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                tipo = request.POST["tipo"]
                techo = request.POST["techo"]
                porcentaje_e = request.POST["porcentaje_e"]
                valor_e = request.POST["valor_e"]
                porcentaje_p = request.POST["porcentaje_p"]
                valor_p = request.POST["valor_p"]
                activo = int(request.POST["activo"])

                if len(tipo) == 0:
                    mensaje = "El campo 'Tipo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(techo) == 0:
                    mensaje = "El campo 'Techo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(porcentaje_e) == 0:
                    mensaje = "El campo 'Porcentaje Empleado' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor_e) == 0:
                    mensaje = "El campo 'Valor Empleado' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(porcentaje_p) == 0:
                    mensaje = "El campo 'Porcentaje Patrono' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor_p) == 0:
                    mensaje = "El campo 'Valor Patrono' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo) > 50:
                    mensaje = "El campo 'Tipo' tiene como máximo 50 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(techo) > 70:
                    mensaje = "El campo 'Techo' tiene como máximo 50 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(porcentaje_e) > 50:
                    mensaje = "El campo 'Porcentaje Empleado' tiene como máximo 50 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor_e) > 50:
                    mensaje = (
                        "El campo 'Valor Empleado' tiene como máximo 50 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(porcentaje_p) > 50:
                    mensaje = (
                        "El campo 'Porcentaje Patrono' tiene como máximo 50 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor_p) > 50:
                    mensaje = (
                        "El campo 'Valor Patrono' tiene como máximo 50 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(techo):
                    mensaje = "El campo 'Techo' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(porcentaje_e):
                    mensaje = "El campo 'Porcentaje Empleado' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor_e):
                    mensaje = "El campo 'Valor Empleado' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(porcentaje_p):
                    mensaje = "El campo 'Porcentaje patrono' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor_p):
                    mensaje = "El campo 'Valor Patrono' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = SeguroSocial(
                    tipo=tipo,
                    techo=techo,
                    porcentaje_e=porcentaje_e,
                    valor_e=valor_e,
                    porcentaje_p=porcentaje_p,
                    valor_p=valor_p,
                    total_p=float(porcentaje_e) + float(porcentaje_p),
                    total_v=float(valor_e) + float(valor_p),
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def segurosocial_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                tipo = request.POST["tipo"]
                techo = request.POST["techo"]
                porcentaje_e = request.POST["porcentaje_e"]
                valor_e = request.POST["valor_e"]
                porcentaje_p = request.POST["porcentaje_p"]
                valor_p = request.POST["valor_p"]
                activo = int(request.POST["activo"])

                if len(tipo) == 0:
                    mensaje = "El campo 'Tipo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(techo) == 0:
                    mensaje = "El campo 'Techo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(porcentaje_e) == 0:
                    mensaje = "El campo 'Porcentaje Empleado' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor_e) == 0:
                    mensaje = "El campo 'Valor Empleado' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(porcentaje_p) == 0:
                    mensaje = "El campo 'Porcentaje Patrono' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor_p) == 0:
                    mensaje = "El campo 'Valor Patrono' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo) > 50:
                    mensaje = "El campo 'Tipo' tiene como máximo 50 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(techo) > 70:
                    mensaje = "El campo 'Techo' tiene como máximo 50 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(porcentaje_e) > 50:
                    mensaje = "El campo 'Porcentaje Empleado' tiene como máximo 50 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor_e) > 50:
                    mensaje = (
                        "El campo 'Valor Empleado' tiene como máximo 50 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(porcentaje_p) > 50:
                    mensaje = (
                        "El campo 'Porcentaje Patrono' tiene como máximo 50 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(valor_p) > 50:
                    mensaje = (
                        "El campo 'Valor Patrono' tiene como máximo 50 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(techo):
                    mensaje = "El campo 'Techo' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(porcentaje_e):
                    mensaje = "El campo 'Porcentaje Empleado' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor_e):
                    mensaje = "El campo 'Valor Empleado' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(porcentaje_p):
                    mensaje = "El campo 'Porcentaje patrono' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(valor_p):
                    mensaje = "El campo 'Valor Patrono' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = SeguroSocial.objects.get(pk=id)
                if oMd:
                    oMd.tipo = tipo
                    oMd.techo = techo
                    oMd.porcentaje_e = porcentaje_e
                    oMd.valor_e = valor_e
                    oMd.porcentaje_p = porcentaje_p
                    oMd.valor_p = valor_p
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def segurosocial_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = SeguroSocial.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------AJAX-------------------------------

# endregion

# region Código para Rap


def rap_listado(request):
    return render(request, "rap.html")


def obtener_rap(request):
    lista = []
    datos = []
    data = {}
    try:
        suc = Branch.objects.get(pk=request.session["sucursal"])
        lista = RapDeduccion.objects.filter(empresa_reg=suc.empresa)
        lista = RapDeduccion.objects.filter()
        for item in lista:

            o_dato = {
                "id": item.pk,
                "techo": item.techo,
                "porcentaje": item.porcentaje,
                "active": "SI" if item.active else "NO",
            }
            datos.append(o_dato)
        data = {"data": datos}
        return JsonResponse(data, safe=False, status=200)
    except Exception as ex:
        data = {"error": str(ex)}
        print(data)
        return JsonResponse(data, safe=False, status=500)


def obtener_reg_rap(request):
    try:
        data = {}
        if "id" in request.GET:
            reg_id = request.GET.get("id")
            reg_id = int(reg_id)
            o_rap = RapDeduccion.objects.get(pk=reg_id)
            data = {
                "pk": o_rap.pk,
                "techo": o_rap.techo,
                "porcentaje": o_rap.porcentaje,
            }
            data = {"error": False, "data": data, "msg": "¡Exito!"}
        else:
            data = {"error": True, "msg": "No se esta pasando el parámetro"}
    except Exception as ex:
        data = {"error": True, "msg": str(ex)}
    return JsonResponse(data, status=200)


def guardar_rap(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["rap_id"]
                techo = request.POST["txttecho"]
                porcentaje = request.POST["txtporcentaje"]
                suc = Branch.objects.get(pk=request.session["sucursal"])
                if len(techo) == 0:
                    mensaje = "El campo 'Techo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)
                if len(porcentaje) == 0:
                    mensaje = "El campo 'Porcentaje' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(reg_id) > 0:
                    if int(reg_id) > 0:
                        o_rap = RapDeduccion.objects.get(pk=reg_id)
                        o_rap.techo = techo
                        o_rap.porcentaje = porcentaje
                        o_rap.user_mod = request.user
                        o_rap.date_mod = datetime.datetime.now()
                        o_rap.save()
                        data = {
                            "error": False,
                            "mensaje": "Se ha actualizado el registro",
                        }
                        return JsonResponse(data)
                    else:
                        data = {
                            "error": True,
                            "mensaje": "No hay registro para modificar",
                        }
                        return JsonResponse(data)
                else:
                    o_Rap = RapDeduccion(
                        techo=techo,
                        porcentaje=porcentaje,
                        empresa_reg=suc.empresa,
                        user_reg=request.user,
                        active=True,
                    )
                    o_Rap.save()
                    return JsonResponse(
                        {"error": False, "mensaje": "Se guardó el registro"},
                        safe=False,
                        status=200,
                    )
            else:
                return JsonResponse(
                    {"error": True, "mensaje": "Método no permitido"},
                    safe=False,
                    status=500,
                )
        else:
            return JsonResponse(
                {"error": True, "mensaje": "Petición no asíncrona"},
                safe=False,
                status=500,
            )
    except Exception as ex:
        pass


def eliminar_rap(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = RapDeduccion.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": str(ex),
        }
    return JsonResponse(data)


# endregion

# region Código para Salario Mínimo


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_segurosocial", raise_exception=True)
def salariominimo_listado(request):
    salarios = []
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_ingresogeneral"):
        lista = SalarioMinimo.objects.filter(empresa_reg=suc.empresa)
    else:
        lista = SalarioMinimo.objects.filter(empresa_reg=suc.empresa, active=True)

    for item in lista:
        dato = {
            "pk": item.pk,
            "fecha": item.fecha,
            "salario_minimo": formato_millar(item.salario_minimo),
            "forzar_salario": item.forzar_salario,
            "vigente": item.vigente,
            "active": item.active,
        }
        salarios.append(dato)
    return render(request, "salariominimo-listado.html", {"lista": salarios})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_ingresogeneral", raise_exception=True)
def salariominimo_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    tipos_ingresos = TipoIngreso.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(
        request, "salariominimo-form.html", {"tipos_ingresos": tipos_ingresos}
    )


# ---------------------AJAX-------------------------------


def salariominimo_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                salario_minimo = request.POST["salario_minimo"]
                forzar_salario = request.POST["forzar_salario"]
                activo = int(request.POST["activo"])

                if len(salario_minimo) == 0:
                    mensaje = "El campo 'Salario Minimo' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                salario_minimo = salario_minimo.replace(",", "")

                if not validarDecimal(salario_minimo):
                    mensaje = "El campo 'Salario Mínimo' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if salario_minimo == 0:
                    mensaje = "El campo 'Salario Mínimo' debe ser mayor a cero(0)."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = SalarioMinimo(
                    salario_minimo=salario_minimo,
                    vigente=True,
                    forzar_salario=forzar_salario,
                    active=activo,
                    empresa_reg=suc.empresa,
                    sucursal_reg=suc,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def salariominimo_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = SalarioMinimo.objects.get(pk=reg_id)
                    if oMd:
                        suc = Branch.objects.get(pk=request.session["sucursal"])
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                        salarios = SalarioMinimo.objects.filter(
                            active=True, empresa_reg=suc.empresa
                        )
                        if salarios.count() > 0:
                            salario = salarios[0]
                            salario.vigente = True
                            salario.user_mod = request.user
                            salario.date_mod = datetime.datetime.now()
                            salario.save()
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------AJAX-------------------------------

# endregion

# region Código para Tipo de Deducciones


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_tipodeduccion", raise_exception=True)
def tipo_deduccion_listado(request):
    listado = []
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_tipodeduccion"):
        listado = TipoDeduccion.objects.filter(empresa_reg=suc.empresa)
    else:
        if request.user.has_perm("worksheet.see_tipodeduccion"):
            listado = TipoDeduccion.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "tipo-deduccion-listado.html", {"listado": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_tipodeduccion", raise_exception=True)
def tipo_deduccion_form(request):
    return render(request, "tipo-deduccion-form.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_tipodeduccion", raise_exception=True)
def tipo_deduccion_editar(request, id):
    dato = TipoDeduccion.objects.get(pk=id)
    return render(request, "tipo-deduccion-form.html", {"dato": dato, "editar": True})


# ---------------------AJAX-------------------------------


def tipo_deduccion_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                tipo_deduccion = request.POST["tipo_deduccion"]
                desc = request.POST["descripcion"]
                activo = int(request.POST["activo"])

                if len(tipo_deduccion) == 0:
                    mensaje = "El campo 'Tipo de Deducción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_deduccion) > 50:
                    mensaje = (
                        "El campo 'Tipo de Deducción' tiene como máximo 50 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = TipoDeduccion(
                    tipo_deduccion=tipo_deduccion,
                    descripcion=desc,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def tipo_deduccion_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                tipo_deduccion = request.POST["tipo_deduccion"]
                desc = request.POST["descripcion"]
                activo = int(request.POST["activo"])

                if len(tipo_deduccion) == 0:
                    mensaje = "El campo 'Tipo de Deducción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_deduccion) > 100:
                    mensaje = (
                        "El campo 'Tipo de Deduccion' tiene como máximo 50 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = TipoDeduccion.objects.get(pk=id)
                if oMd:
                    oMd.tipo_deduccion = tipo_deduccion
                    oMd.descripcion = desc
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def tipo_deduccion_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = TipoDeduccion.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------AJAX-------------------------------

# endregion

# region Código para Tipo de Nomina


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_tiponomina", raise_exception=True)
def tipo_nomina_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    listado = TipoNomina.objects.filter(empresa_reg=suc.empresa)
    return render(request, "tipo-nomina-listado.html", {"listado": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_tiponomina", raise_exception=True)
def tipo_nomina_form(request):
    return render(request, "tipo-nomina-form.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_tiponomina", raise_exception=True)
def tipo_nomina_editar(request, id):
    dato = TipoNomina.objects.get(pk=id)
    return render(request, "tipo-nomina-form.html", {"dato": dato, "editar": True})


# ---------------------AJAX-------------------------------


def tipo_nomina_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                tipo_nomina = request.POST["tipo_nomina"]
                desc = request.POST["descripcion"]
                activo = int(request.POST["activo"])

                if len(tipo_nomina) == 0:
                    mensaje = "El campo 'Tipo Nómina' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_nomina) > 100:
                    mensaje = "El campo 'Tipo Nómina' tiene como máximo 100 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = TipoNomina(
                    tipo_planilla=tipo_nomina,
                    descripcion=desc,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def tipo_nomina_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                tipo_nomina = request.POST["tipo_nomina"]
                desc = request.POST["descripcion"]
                activo = int(request.POST["activo"])

                if len(tipo_nomina) == 0:
                    mensaje = "El campo 'Tipo Nómina' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_nomina) > 100:
                    mensaje = "El campo 'Tipo Nómina' tiene como máximo 100 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = TipoNomina.objects.get(pk=id)
                if oMd:
                    oMd.tipo_planilla = tipo_nomina
                    oMd.descripcion = desc
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def tipo_nomina_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = TipoNomina.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------END AJAX---------------------------

# endregion

# region Código para Tipo de Ingreso


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_tipoingreso", raise_exception=True)
def tipo_ingreso_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista = TipoIngreso.objects.filter(empresa_reg=suc.empresa)
    return render(request, "tipo-ingreso-listado.html", {"lista": lista})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_tipoingreso", raise_exception=True)
def tipo_ingreso_form(request):
    return render(request, "tipo-ingreso-form.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_tipoingreso", raise_exception=True)
def tipo_ingreso_editar(request, id):
    dato = TipoIngreso.objects.get(pk=id)
    return render(request, "tipo-ingreso-form.html", {"dato": dato, "editar": True})


# ---------------------AJAX-------------------------------


def tipo_ingreso_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                tipo_ingreso = request.POST["tipo_ingreso"]
                desc = request.POST["descripcion"]
                orden = request.POST["orden"]
                activo = int(request.POST["activo"])

                if len(tipo_ingreso) == 0:
                    mensaje = "El campo 'Tipo Ingreso' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_ingreso) > 100:
                    mensaje = (
                        "El campo 'Tipo Ingreso' tiene como máximo 100 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if orden == 0:
                    mensaje = "El valor del campo 'Orden' tiene que ser mayor a cero(0)"
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = TipoIngreso(
                    tipo_ingreso=tipo_ingreso,
                    descripcion=desc,
                    empresa_reg=suc.empresa,
                    orden=orden,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def tipo_ingreso_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                tipo_ingreso = request.POST["tipo_ingreso"]
                desc = request.POST["descripcion"]
                orden = request.POST["orden"]
                activo = int(request.POST["activo"])

                if len(tipo_ingreso) == 0:
                    mensaje = "El campo 'Tipo Ingreso' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_ingreso) > 100:
                    mensaje = (
                        "El campo 'Tipo Ingreso' tiene como máximo 100 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if orden == 0:
                    mensaje = "El campo 'Orden' tiene que ser mayor a cero(0)."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = TipoIngreso.objects.get(pk=id)
                if oMd:
                    oMd.tipo_ingreso = tipo_ingreso
                    oMd.descripcion = desc
                    oMd.orden = orden
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def tipo_ingreso_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = TipoIngreso.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------AJAX-------------------------------
# endregion

# region Código para Impuesto Vecinal


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_impuestosobrerenta", raise_exception=True)
def impuestovecinal_listado(request):
    listado = []
    dato = {}
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_impuestovecinal"):
        lista = ImpuestoVecinal.objects.filter(empresa_reg=suc.empresa)

    else:
        lista = ImpuestoVecinal.objects.filter(empresa_reg=suc.empresa, active=True)
    for item in lista:
        dato = {
            "pk": item.pk,
            "desde": formato_millar(item.desde),
            "hasta": formato_millar(item.hasta),
            "porcentaje_label": formato_millar(item.porcentaje) + "%",
            "active": item.active,
        }
        listado.append(dato)
    return render(request, "impuestovecinal-listado.html", {"lista": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_impuestovecinal", raise_exception=True)
def impuestovecinal_form(request):
    return render(request, "impuestovecinal-form.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_segurosocial", raise_exception=True)
def impuestovecinal_editar(request, id):
    dato = ImpuestoVecinal.objects.get(pk=id)
    return render(request, "impuestovecinal-form.html", {"dato": dato, "editar": True})


# ---------------------AJAX-------------------------------


def impuestovecinal_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                desde = request.POST["desde"]
                hasta = request.POST["hasta"]
                porcentaje = request.POST["porcentaje"]
                activo = int(request.POST["activo"])

                desde = desde.replace(",", "")
                hasta = hasta.replace(",", "")
                porcentaje = porcentaje.replace("%", "")

                if len(desde) == 0:
                    mensaje = "El campo 'Desde' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(hasta) == 0:
                    mensaje = "El campo 'Hasta' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(desde):
                    mensaje = "El campo 'Desde' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(hasta):
                    mensaje = "El campo 'Hasta' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(porcentaje):
                    mensaje = "El campo 'Porcentaje' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = ImpuestoVecinal(
                    desde=desde,
                    hasta=hasta,
                    porcentaje=porcentaje,
                    porcentaje_label=str(porcentaje) + "%",
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        print(ex)
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def impuestovecinal_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                desde = request.POST["desde"]
                hasta = request.POST["hasta"]
                porcentaje = request.POST["porcentaje"]
                activo = int(request.POST["activo"])

                if len(desde) == 0:
                    mensaje = "El campo 'Desde' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(hasta) == 0:
                    mensaje = "El campo 'Hasta' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                desde = desde.replace(",", "")
                hasta = hasta.replace(",", "")
                porcentaje = porcentaje.replace(",", "")
                porcentaje = porcentaje.replace("%", "")

                if not validarDecimal(desde):
                    mensaje = "El campo 'Desde' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(hasta):
                    mensaje = "El campo 'Hasta' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if not validarDecimal(porcentaje):
                    mensaje = "El campo 'Porcentaje' es de tipo decimal."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = ImpuestoVecinal.objects.get(pk=id)
                if oMd:
                    oMd.desde = desde
                    oMd.hasta = hasta
                    oMd.porcentaje = porcentaje
                    oMd.porcentaje_label = str(porcentaje) + "%"
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def impuestovecinal_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = ImpuestoVecinal.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


# ---------------------AJAX-------------------------------

# endregion

# region Código para Tipo de Contrato


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.see_tipocontrato", raise_exception=True)
def tipo_contrato_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_tipocontrato"):
        listado = TipoContrato.objects.filter(empresa_reg=suc.empresa)
    else:
        listado = TipoContrato.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, "tipo-contrato-listado.html", {"listado": listado})


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.add_tipocontrato", raise_exception=True)
def tipo_contrato_form(request):
    return render(request, "tipo-contrato-form.html")


@login_required(login_url="/form/iniciar-sesion/")
@permission_required("worksheet.change_tipocontrato", raise_exception=True)
def tipo_contrato_editar(request, id):
    dato = TipoContrato.objects.get(pk=id)
    return render(request, "tipo-contrato-form.html", {"editar": True, "dato": dato})


# ---------------------AJAX-------------------------------


def tipo_contrato_guardar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                tipo_contrato = request.POST["tipo_contrato"]
                desc = request.POST["descripcion"]
                activo = int(request.POST["activo"])

                if len(tipo_contrato) == 0:
                    mensaje = "El campo 'Tipo de Contrato' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_contrato) > 100:
                    mensaje = (
                        "El campo 'Tipo Contrato' tiene como máximo 100 caracteres."
                    )
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = TipoContrato(
                    tipo_contrato=tipo_contrato,
                    descripcion=desc,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = "Se ha guardado el registro"
                data = {"mensaje": mensaje, "error": False}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def tipo_contrato_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                id = int(request.POST["id"])
                tipo_contrato = request.POST["tipo_contrato"]
                desc = request.POST["descripcion"]
                activo = int(request.POST["activo"])

                if len(tipo_contrato) == 0:
                    mensaje = "El campo 'Tipo Nómina' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if len(tipo_contrato) > 100:
                    mensaje = "El campo 'Tipo Nómina' tiene como máximo 100 caracteres."
                    data = {"error": True, "mensaje": mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = TipoContrato.objects.get(pk=id)
                if oMd:
                    oMd.tipo_contrato = tipo_contrato
                    oMd.descripcion = desc
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = "Se ha actualizado el registro."
                    data = {"mensaje": mensaje, "error": False}
                else:
                    mensaje = "No existe el registro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "No es una petición AJAX."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def tipo_contrato_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == "POST":
                reg_id = request.POST["id"]
                if int(reg_id) > 0:
                    oMd = TipoContrato.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = "Se ha eliminado el registro."
                        data = {"mensaje": mensaje, "error": False}
                    else:
                        mensaje = "No existe el registro."
                        data = {"mensaje": mensaje, "error": True}
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {"mensaje": mensaje, "error": True}
            else:
                mensaje = "Método no permitido."
                data = {"mensaje": mensaje, "error": True}
        else:
            mensaje = "Tipo de petición no permitido."
            data = {"mensaje": mensaje, "error": True}
    except Exception as ex:
        data = {
            "error": True,
            "mensaje": "error",
        }
    return JsonResponse(data)


def boleta_pago_reporte(request):
    empleado_id = request.GET.get("empleado_id")
    planilla_id = request.GET.get("planilla_id")
    detalles = []
    o_empleado = Employee.objects.get(pk=empleado_id)
    o_planilla = Planilla.objects.get(pk=planilla_id)
    o_pla_de_ing = PlanillaDetalleIngresos.objects.filter(
        empleado=o_empleado, planilla=o_planilla
    ).order_by('tipo_ingreso__indice_relevancia')
    o_pla_de_ded = PlanillaDetalleDeducciones.objects.filter(
        empleado=o_empleado, planilla=o_planilla
    ).order_by('tipo_deduccion__indice_relevancia')
    response = HttpResponse(content_type="application/pdf")
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setTitle("Boleta de Pago - Promaco")
    pdf.setPageSize((225, 400))
    archivo_imagen = settings.MEDIA_ROOT + "/imagenes/promaco-logo.png"
    pdf.drawImage(archivo_imagen, 65, 350, 100, 60, preserveAspectRatio=True)
    pdf.setFont("Helvetica", 14)
    pdf.drawString(65, 340, "Boleta de Pago")
    pdf.setFont("Helvetica", 7)
    pdf.drawString(15, 320, "Empleado: ")
    Nombre = o_empleado.firstName
    if o_empleado.middleName:
        Nombre += " " + o_empleado.middleName
    Nombre += " " + o_empleado.lastName
    pdf.setFont("Helvetica", 7)
    pdf.drawString(50, 320, Nombre)
    pdf.setFont("Helvetica", 7)
    pdf.drawString(15, 310, "Fecha de pago: ")
    pdf.setFont("Helvetica", 7)
    pdf.drawString(65, 310, datetime.datetime.strftime(o_planilla.fecha_pago, "%d/%m/%Y"))

    punto_tabla = 240
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.fontSize = 7
    encabezados = ("Descripción", "Ingreso", "Deducc.")
    posicionTabla = 280
    for fila in o_pla_de_ing:
        detalles.append(
            [Paragraph(fila.ingreso, styleN), formato_millar(fila.valor), 0.00]
        )
        posicionTabla -= 20

    for fila in o_pla_de_ded:
        detalles.append(
            [Paragraph(fila.deduccion, styleN), 0.00, formato_millar(fila.valor)]
        )
        posicionTabla -= 10
    # detalles = [(Paragraph(fila.ingreso, styleN), formato_millar(fila.valor), 0.00) for fila in o_pla_de_ing]
    # detalles += [(Paragraph(fila.deduccion, styleN),0.00, formato_millar(fila.valor)) for fila in o_pla_de_ded]
    detalle_pagos = Table(
        [encabezados] + detalles, colWidths=[3.2 * cm, 1.8 * cm, 1.8 * cm]
    )
    detalle_pagos.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (2, 0), "CENTER"),
                ("ALIGN", (1, 1), (2, -1), "RIGHT"),
                ("FONTSIZE", (0, 1), (-1, -1), 7),
                ("INNERGRID", (0, 0), (-1, -1), 0.10, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.10, colors.black),
                ("VALIGN", (0, 1), (-1, -1), "MIDDLE"),
            ]
        )
    )
    detalle_pagos.wrapOn(pdf, 190, 10)
    detalle_pagos.drawOn(pdf, 15, posicionTabla)
    pdf.setFont("Helvetica", 8)
    pdf.drawString(15, 250, "Sueldo Neto: ")

    pdf.showPage()
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def boleta_pago_email(request):
    image_path = '././static/images/promaco-logo.png'
    image_name = Path(image_path).name
    empleado_id = request.GET.get("empleado_id")
    planilla_id = request.GET.get("planilla_id")
    detalles = []
    o_empleado = Employee.objects.get(pk=empleado_id)
    o_planilla = Planilla.objects.get(pk=planilla_id)
    o_pla_de_ing = PlanillaDetalleIngresos.objects.filter(
        empleado=o_empleado, planilla=o_planilla
    )
    o_pla_de_ded = PlanillaDetalleDeducciones.objects.filter(
        empleado=o_empleado, planilla=o_planilla
    )
    empleado_id = request.GET.get("empleado_id")
    planilla_id = request.GET.get("planilla_id")
    detalle_ing = []
    detalle_ded = []
    o_empleado = Employee.objects.get(pk=empleado_id)
    o_planilla = Planilla.objects.get(pk=planilla_id)
    o_pla_de_ing = PlanillaDetalleIngresos.objects.filter(
        empleado=o_empleado, planilla=o_planilla
    )
    o_pla_de_ded = PlanillaDetalleDeducciones.objects.filter(
        empleado=o_empleado, planilla=o_planilla
    )
    o_pla_de = PlanillaDetalle.objects.get(empleado=o_empleado, planilla=o_planilla)
    for item in o_pla_de_ing:
        data = {"ingreso": item.ingreso, "valor": formato_millar(item.valor)}
        detalle_ing.append(data)
    for item in o_pla_de_ded:
        data = {
            "deduccion": item.deduccion,
            "valor": formato_millar(item.valor),
        }
        detalle_ded.append(data)
    asunto, remite, destinatario = (
        "Boleta de Pago",
        "no-replay@gmail.com",
        o_empleado.email,
    )
    # html_message = f"""<!DOCTYPE html>"
    # "<html lang='es'>"
    # "<head>"
    # "<meta chartse='UTF-8'>"
    # "<title>Some title</title>"""
    # html_message += ("<style>"
    #         " *{padding; 0; margin; 0;}"
    #         " h1{text-align:center;}"
    #         " img{width: 100px;}"
    #         "</style>")
    # html_message += f"""<body>"
    # "<div class='contenido'>"
    # "<img src='cid:{image_name}' />"
    # "<h1>Boleta de Pago</h1>"
    # "</div>"
    # "</body>"
    # "</head>"
    # "</html>"""
    html_contenido_txt = render_to_string(
        "correo/boleta_pago_text.txt",
        {
            "empleado": o_empleado,
            "detalle": o_pla_de,
            "planilla": o_planilla,
            "dias_trabajados": int(o_pla_de.dias_salario) - int(o_pla_de.dias_ausentes_sin_pago),
            "detalle_ingreso": detalle_ing,
            "detalle_deduccion": detalle_ded,
            "logo": 'cid:{image_name}',
            "total_ingreso": formato_millar(o_pla_de.total_ingresos),
            "total_deduccion": formato_millar(o_pla_de.total_deducciones),
            "sueldo_neto": formato_millar(
                o_pla_de.total_ingresos - o_pla_de.total_deducciones
            ),
        },
    )
    html_contenido = render_to_string(
        "correo/boleta_pago_html.html",
        {
            "empleado": o_empleado,
            "detalle": o_pla_de,
            "planilla": o_planilla,
            "dias_trabajados": int(o_pla_de.dias_salario) - int(o_pla_de.dias_ausentes_sin_pago),
            "detalle_ingreso": detalle_ing,
            "detalle_deduccion": detalle_ded,
            "logo": 'cid:{image_name}',
            "total_ingreso": formato_millar(o_pla_de.total_ingresos),
            "total_deduccion": formato_millar(o_pla_de.total_deducciones),
            "sueldo_neto": formato_millar(
                o_pla_de.total_ingresos - o_pla_de.total_deducciones
            ),
        },
    )
    #text_contenido = strip_tags(html_contenido)
    msg = EmailMultiAlternatives(asunto, html_contenido_txt, remite, [destinatario])
    #msg = EmailMultiAlternatives(asunto, html_message, remite, [destinatario])
    if all([html_contenido, image_path, image_name]):
        msg.attach_alternative(html_contenido, "text/html")
        #msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'

        with open(image_path, mode='rb')as f:
            image = MIMEImage(f.read())
            image.add_header('Content-ID', f"<{image_name}>")
            msg.attach(image)
    msg.send()
    data = {"error": True, "mensaje": "El email se ha enviado"}
    return JsonResponse(data)

def boleta_pago_email_masivo(ingresos, deducciones, empleado, planilla, detalle):
    detalle_ing = []
    detalle_ded = []
    for item in ingresos:
        data = {"ingreso": item.ingreso, "valor": formato_millar(item.valor)}
        detalle_ing.append(data)
    for item in deducciones:
        data = {
            "deduccion": item.deduccion,
            "valor": formato_millar(item.valor),
        }
        detalle_ded.append(data)
    asunto, remite, destinatario = (
        "Boleta de Pago",
        "no-replay@gmail.com",
        empleado.email,
    )
    print(empleado.firstName)
    html_contenido = render_to_string(
        "correo/boleta_pago_html.html",
        {
            "empleado": empleado,
            "detalle": detalle,
            "planilla": planilla,
            "dias_trabajados": int(detalle.dias_salario) - int(detalle.dias_ausentes_sin_pago),
            "detalle_ingreso": detalle_ing,
            "detalle_deduccion": detalle_ded,
            "total_ingreso": formato_millar(detalle.total_ingresos),
            "total_deduccion": formato_millar(detalle.total_deducciones),
            "sueldo_neto": formato_millar(
                detalle.total_ingresos - detalle.total_deducciones
            ),
        },
    )
    text_contenido = strip_tags(html_contenido)
    msg = EmailMultiAlternatives(asunto, text_contenido, remite, [destinatario])
    msg.attach_alternative(html_contenido, "text/html")
    #msg.send()
    # data = {"error": True, "mensaje": "El email se ha enviado"}
    # return JsonResponse(data)


def reporte_probando(request):
    template = get_template("correo/boleta_pago_html.html")
    context = {
        "nombre": "Malco Baquedano",
    }
    html = template.render(context)
    return HttpResponse(html)


# ---------------------END AJAX---------------------------

# endregion

# region Código para Deducciones Empleados
def deducciones_empleado_listado(request):
    if not "sucursal" in request.session:
        return HttpResponseRedirect("/salir/")
    else:
        if int(request.session["sucursal"]) < 1:
            return HttpResponseRedirect("/salir/")
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(branch=suc, active=True).order_by("firstName")
    empleados_l= Employee.objects.filter(branch=suc).order_by("first_name")
    planillas = Planilla.objects.filter(cerrada=False, sucursal_reg=suc, active=True)
    planillas_l = Planilla.objects.filter(sucursal_reg=suc, active=True)
    tipos_deduccion = DeduccionTipo.objects.filter(active=True, visible=True)
    return render(
        request,
        "deducciones-empleado.html",
        {
            "empleados": empleados,
            "planillas": planillas,
            'planillas_l':planillas_l,
            "tipos_deduccion": tipos_deduccion,
        },
    )


# <<<<<<<<<<<<<<< AJAX >>>>>>>>>>>>>>>>>>>>


@login_required(login_url="/form/iniciar-sesion/")
def deducciones_empleado_filtro_obtener(request):
    data = {}
    data_l = []
    q_list = []
    total_monto = 0
    try:
        empleado_id = request.GET.get("empleado")
        planilla_id = request.GET.get("planilla")
        tipo_deduccion_id = request.GET.get("deduccion")

        if len(empleado_id) > 0:
            if int(empleado_id) > 0:
                empleado_obj = Employee.objects.get(pk=empleado_id)
                print(empleado_obj.active)
                if empleado_obj.active:
                    q_list.append(Q(empleado__pk=empleado_id))
                else:
                    return JsonResponse({
                        "error": True,
                        "mensaje": "El empleado asignado a la deducción no está activo."
                    })


        if len(planilla_id) > 0:
            if int(planilla_id) > 0:
                q_list.append(Q(planilla__pk=planilla_id))

        if len(tipo_deduccion_id) > 0:
            if int(tipo_deduccion_id) > 0:
                q_list.append(Q(deduccion__pk=tipo_deduccion_id))

        datos = DeduccionEmpleado.objects.filter(
            functools.reduce(operator.and_, q_list)
        ).order_by('empleado', 'deduccion')
        for item in datos:
            empleado = item.empleado.firstName
            if item.empleado.middleName:
                empleado += " " + item.empleado.middleName
            empleado += " " + item.empleado.lastName
            obj = {
                "id": item.pk,
                "codigo": item.empleado.extEmpNo,
                "empleado": empleado,
                "deduccion": item.deduccion.deduccion_tipo,
                "monto": formato_millar(item.monto),
                "detalle": item.detalle,
                "active": item.active,
            }
            data_l.append(obj)
            total_monto += item.monto
        data = {
            "mensaje": "¡Proceso Exitoso!",
            "deducciones": data_l,
            "total_deduccion": formato_millar(total_monto),
            "error": False,
        }
    except Exception as e:
        data = {"mensaje": str(e), "error": True}

    return JsonResponse(data)

def deducciones_empleado_registro_obtener(request):
    data = {}
    det_l = []
    try:
        tot_det = 0
        id = request.GET.get("id")
        obj = DeduccionEmpleado.objects.get(pk=id)
        if not obj.empleado.active:
            return JsonResponse({'error':True, 'mensaje': 'El empleado no está activo'})
        elif obj.planilla.cerrada:
            return JsonResponse({'error':True, 'mensaje': 'La planilla está cerrada'})
        dets = DeduccionIndividualSubDetalle.objects.filter(deduccion=obj)

        for detalle in dets:
            tot_det += detalle.monto
            obj_E = {
                'id':detalle.id,
                'descripcion': detalle.descripcion,
                'monto': formato_millar(detalle.monto),
                'fecha': datetime.datetime.strftime(detalle.fecha, "%d/%m/%Y"),
            }
            det_l.append(obj_E)
        obj_V = {
            "id": obj.pk,
            "empleado": obj.empleado.id,
            "planilla": obj.planilla.id,
            "deduccion": obj.deduccion.id,
            "monto": obj.monto,
            "detalle": det_l,
            "detalle_total": formato_millar(tot_det),
            "active": obj.active,
        }
        data = {"mensaje": "Exito", "error": False, "dato": obj_V}
    except Exception as e:
        data = {"mensaje": str(e), "error": True}
    return JsonResponse(data)

def deducciones_empleado_guardar(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                data = json.loads(request.body.decode("utf-8"))
                planilla_id = data["planilla"]
                empleado_id = data["empleado"]
                deduccion_id = data["deduccion"]
                monto = data["monto"]
                detalle = data["detalle"]
                if len(planilla_id) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Planilla"',
                        "error": True,
                    }
                else:
                    if int(planilla_id) == 0:
                        data = {
                            "mensaje": 'No se ha pasado un valor válido para el campo "Planilla"',
                            "error": True,
                        }

                if len(deduccion_id) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Deducción"',
                        "error": True,
                    }
                else:
                    if int(deduccion_id) == 0:
                        data = {
                            "mensaje": 'No se ha pasado un valor válido para el campo "Deducción"',
                            "error": True,
                        }

                if len(empleado_id) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Empleado"',
                        "error": True,
                    }
                else:
                    if int(empleado_id) == 0:
                        data = {
                            "mensaje": 'No se ha pasado un valor válido para el campo "Empleado"',
                            "error": True,
                        }

                if len(monto) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Monto"',
                        "error": True,
                    }
                else:
                    if float(monto) == 0:
                        data = {
                            "mensaje": 'No se ha pasado un valor válido para el campo "Monto"',
                            "error": True,
                        }

                o_planilla = Planilla.objects.get(pk=planilla_id)
                o_deduccion = DeduccionTipo.objects.get(pk=deduccion_id)
                o_empleado = Employee.objects.get(pk=empleado_id)

                cons = DeduccionEmpleado.objects.filter(
                    planilla=o_planilla, empleado=o_empleado, deduccion=o_deduccion
                )
                if cons.exists():
                    data = {
                        "mensaje": "Ya existe la deducción para el empleado en la planilla seleccionada.",
                        "error": True,
                    }
                else:
                    o_bj = DeduccionEmpleado(
                        planilla=o_planilla,
                        deduccion=o_deduccion,
                        empleado=o_empleado,
                        monto=monto,
                        detalle=detalle,
                        user_reg=request.user,
                    )
                    o_bj.save()
                    data = {"mensaje": "Se ha creado el registro.", "error": False}
            else:
                data = {"mensaje": "El método no está permitido", "error": True}
        else:
            data = {
                "mensaje": "El tipo de petición http no está permitido",
                "error": True,
            }
    except Exception as e:
        data = {"mensaje": str(e), "error": True}
    return JsonResponse(data)

def deducciones_empleado_actualizar(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                data = json.loads(request.body.decode("utf-8"))
                id = data["id"]
                monto = data["monto"]
                detalle = data["detalle"]
                active = data["active"]

                if len(monto) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Monto"',
                        "error": True,
                    }
                    return JsonResponse(data)
                else:
                    if float(monto) == 0:
                        data = {
                            "mensaje": 'No se ha pasado un valor válido para el campo "Monto"',
                            "error": True,
                        }
                        return JsonResponse(data)


                obj = DeduccionEmpleado.objects.get(pk=id)
                dedsub = DeduccionIndividualSubDetalle.objects.filter(deduccion=obj)
                if dedsub.exists():
                    if detalle == False:
                        data = {
                            "mensaje": 'La deducción tiene registros en detalle, no se puede actualizar el campo "Requiere detalle" a valor "Falso"',
                            "error": True,
                        }
                        return JsonResponse(data)

                obj.monto = monto
                # obj.detalle = detalle
                obj.active = active
                obj.user_mod = request.user
                #obj.date_mod = datetime.now()
                obj.save()
                data = {"mensaje": "Se ha actualizado el registro", "error": False}
            else:
                data = {"mensaje": "Método no permitido", "error": True}
        else:
            data = {"mensaje": "Tipo de petición no está permitido", "error": True}
    except Exception as e:
        data = {"mensaje": str(e), "error": True}
    return JsonResponse(data)

def deducciones_empleado_eliminar(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                data = json.loads(request.body.decode("utf-8"))
                ded_id = data["id"]
                print(ded_id)
                # if len(ded_id) == 0:
                #     data = {'mensaje': 'No se pasó un valor válido para el registro a eliminar.', 'error':True}
                # else:
                if int(ded_id) == 0:
                    data = {
                        "mensaje": "No se pasó un valor válido para el registro a eliminar.",
                        "error": True,
                    }
                else:
                    o_ded = DeduccionEmpleado.objects.get(pk=ded_id)
                    dedsub = DeduccionIndividualSubDetalle.objects.filter(deduccion=o_ded)
                    planilladed = PlanillaDetalleDeducciones.objects.filter(deduccion_f=o_ded)
                    
                    if dedsub.exists():
                        data = {"mensaje": "La deducción no puede ser eliminada, tiene registros en Detalle", "error": True}
                        return JsonResponse(data)
                    # if planilladed.exists():
                    #     planilladed.delete()
                    o_ded.delete()
                    data = {"mensaje": "El registro ha sido eliminado", "error": False}
            else:
                data = {"mensaje": "El método no está permitido", "error": True}
        else:
            data = {"mensaje": "El tipo de petición no está permitido", "error": True}
    except Exception as e:
        data = {"mensaje": str(e), "error": True}

    return JsonResponse(data)

def deducciones_detalle_empleado_eliminar(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                data = json.loads(request.body.decode("utf-8"))
                ded_id = data["id"]
                
                if int(ded_id) == 0:
                    data = {
                        "mensaje": "No se pasó un valor válido para el registro a eliminar.",
                        "error": True,
                    }
                else:
                    #o_ded = DeduccionEmpleado.objects.get(pk=ded_id)
                    dedsub = DeduccionIndividualSubDetalle.objects.filter(pk=ded_id)
                    dedsub.delete()
                    data = {"mensaje": "El registro ha sido eliminado", "error": False}
            else:
                data = {"mensaje": "El método no está permitido", "error": True}
        else:
            data = {"mensaje": "El tipo de petición no está permitido", "error": True}
    except Exception as e:
        data = {"mensaje": str(e), "error": True}

    return JsonResponse(data)

def deducciones_reversion(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                data = json.loads(request.body.decode("utf-8"))
                planilla_id = data['planilla']
                deduccion_id = data['deduccion']
                if int(planilla_id) == 0:
                    data = {
                        "mensaje": "No se pasó un valor válido en el campo 'Planilla'",
                        "error": True,
                    }
                else:
                    o_planilla = Planilla.objects.get(pk=planilla_id)
                    planilla_detalles = PlanillaDetalle.objects.filter(planilla=o_planilla)
                    if int(deduccion_id) == 0:
                        deducciones_detalle = PlanillaDetalleDeducciones.objects.filter(planilla=o_planilla)
                        deducciones = DeduccionEmpleado.objects.filter(planilla=o_planilla)
                    else:
                        o_tipodeduccion = DeduccionTipo.objects.get(pk=deduccion_id)
                        deducciones_detalle = PlanillaDetalleDeducciones.objects.filter(planilla=o_planilla, tipo_deduccion=o_tipodeduccion)
                        deducciones = DeduccionEmpleado.objects.filter(planilla=o_planilla, deduccion=o_tipodeduccion)
                    if deducciones_detalle:
                        deducciones_detalle.delete()
                    if deducciones:
                        deducciones.delete()
                    data = {
                        "mensaje": "Se han revertido los datos",
                        "error": False,
                    }
            else:
                data = {"mensaje": "El método no está permitido", "error": True}
        else:
            data = {"mensaje": "El tipo de petición no está permitido", "error": True}
    except Exception as e:
        data = {"mensaje": str(e), "error": True}
    return JsonResponse(data)

def deduccion_detalles_guardar(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                data = json.loads(request.body.decode("utf-8"))
                descripcion = data["descripcion"]
                fecha = data["fecha"]
                deduccion_id = data["deduccion"]
                monto = data["monto"]
                if len(descripcion) == '':
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Planilla"',
                        "error": True,
                    }

                if len(fecha) == '':
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Deducción"',
                        "error": True,
                    }

                if float(monto) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Monto"',
                        "error": True,
                    }

                fecha = datetime.datetime.strptime(fecha, "%d/%m/%Y").date()

                o_deduccion = DeduccionEmpleado.objects.get(pk=deduccion_id)
                
                o_bj = DeduccionIndividualSubDetalle(
                    descripcion=descripcion,
                    deduccion=o_deduccion,
                    monto=monto,
                    fecha=fecha,
                    user_reg=request.user,
                )
                o_bj.save()
                data = {"mensaje": "Se ha creado el registro.", "error": False}
            else:
                data = {"mensaje": "El método no está permitido", "error": True}
        else:
            data = {
                "mensaje": "El tipo de petición http no está permitido",
                "error": True,
            }
    except Exception as e:
        data = {"mensaje": str(e), "error": True}
    return JsonResponse(data)

@login_required(login_url="/form/iniciar-sesion/")
def deducciones_empleado_archivo_guardar(request):
    data = {}
    lista_bulk = []
    try:
        if request.is_ajax():
            if request.method == "POST":
                suc = Branch.objects.get(pk=request.session["sucursal"])
                planilla_id = request.POST["planilla_id"]
                tipo_deduccion_id = request.POST["tipo_deduccion"]
                if len(planilla_id) == 0 or planilla_id == "null":
                    data = {
                        "mensaje": "No se pasó un valor válido para el campo planilla",
                        "error": True,
                    }
                    return JsonResponse(data)
                else:
                    if int(planilla_id) == 0:
                        data = {
                            "mensaje": "No se pasó un valor válido para el campo planilla",
                            "error": True,
                        }
                        return JsonResponse(data)

                if len(tipo_deduccion_id) == 0 or tipo_deduccion_id == "null":
                    data = {
                        "mensaje": "No se pasó un valor válido para el campo tipo deducción",
                        "error": True,
                    }
                    return JsonResponse(data)
                else:
                    if int(tipo_deduccion_id) == 0:
                        data = {
                            "mensaje": "No se pasó un valor válido para el campo tipo deducción",
                            "error": True,
                        }
                        return JsonResponse(data)

                form = DeduccionEmpleadoForm(request.POST, request.FILES)
                if form.is_valid():
                    bandera = False
                    tot_reg_mod = 0
                    mensaje = ""
                    datosf = request.FILES["archivo"]
                    df = pandas.read_excel(
                        datosf, sheet_name="Deducciones", usecols=["Codigo", "Monto"]
                    )
                    datos = df.to_dict(orient="record")
                    for item in datos:
                        codigo = item["Codigo"]
                        if Employee.objects.filter(extEmpNo=codigo).exists():
                            o_empleado = Employee.objects.get(
                                extEmpNo=codigo, active=True
                            )
                            if o_empleado.branch != suc:
                                data = {
                                    "mensaje": "El empleado con código "
                                    + str(codigo)
                                    + " no está asignado a la sucursal en sesión.",
                                    "error": True,
                                }
                                bandera = True
                            else:
                                o_planilla = Planilla.objects.get(pk=planilla_id)
                                o_tipo_ded = DeduccionTipo.objects.get(
                                    pk=tipo_deduccion_id
                                )
                                o_ded = DeduccionEmpleado.objects.filter(
                                    empleado=o_empleado,
                                    planilla=o_planilla,
                                    deduccion=o_tipo_ded,
                                )
                                if o_ded.exists():
                                    o_ded = DeduccionEmpleado.objects.get(
                                        empleado=o_empleado,
                                        planilla=o_planilla,
                                        deduccion=o_tipo_ded,
                                    )
                                    o_ded.monto = item["Monto"]
                                    o_ded.save()
                                    tot_reg_mod += 1
                                else:
                                    o_ded = DeduccionEmpleado(
                                        empleado=o_empleado,
                                        planilla=o_planilla,
                                        deduccion=o_tipo_ded,
                                        monto=item["Monto"],
                                        user_reg=request.user,
                                    )
                                    if item["Monto"] > 0:
                                        lista_bulk.append(o_ded)
                        else:
                            data = {
                                "mensaje": "El empleado con código "
                                + str(codigo)
                                + " no existe.",
                                "error": True,
                            }
                            bandera = True
                        if bandera:
                            return JsonResponse(data)

                    DeduccionEmpleado.objects.bulk_create(lista_bulk)
                    if len(lista_bulk) > 0:
                        mensaje = (
                            "Se han cargado " + str(len(lista_bulk)) + " registros. "
                        )
                    if tot_reg_mod > 0:
                        mensaje += (
                            "Se ha modificado " + str(tot_reg_mod) + " registros."
                        )
                    data = {"mensaje": mensaje, "error": False}
                else:
                    data = {"mensaje": "Datos incompletos", "error": True}
            else:
                data = {"mensaje": "El método no es válido.", "error": True}
        else:
            data = {"mensaje": "La petición no es asíncrona", "error": True}
    except Exception as e:
        data = {"mensaje": str(e), "error": True}

    return JsonResponse(data)


# <<<<<<<<<<<<<<< AJAX >>>>>>>>>>>>>>>>>>>>
# endregion

# region Código para Deducciones Tipo


@login_required(login_url="/form/iniciar-sesion/")
def deducciones_tipos(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(branch=suc).order_by("firstName")
    deducciones = DeduccionTipo.objects.all().order_by("deduccion_tipo")
    return render(
        request,
        "deducciones_tipos.html",
        {"empleados": empleados, "deducciones": deducciones},
    )


# --------------------AJAX-----------------------


def deduccion_tipo_obtener(request):
    data = {}
    id = request.GET.get("id")
    obj = DeduccionTipo.objects.get(pk=id)
    data = {
        "id": obj.pk,
        "deduccion_tipo": obj.deduccion_tipo,
        "es_legal": obj.es_legal,
        "es_externa": obj.es_externa,
        "indice_relevancia": obj.indice_relevancia,
        "active": obj.active,
    }
    return JsonResponse(data)


def deducciones_tipos_listado(request):
    data = {}
    lista = []
    try:
        data = DeduccionTipo.objects.all()
        for item in data:
            objeto = {
                "id": item.pk,
                "deduccion_tipo": item.deduccion_tipo,
                "es_legal": item.es_legal,
                "es_externa": item.es_externa,
                "indice_relevancia": item.indice_relevancia,
                "active": item.active,
            }
            lista.append(objeto)
        data = {"mensaje": "Operación finalizada correctamente", "datos": lista}
    except Exception as e:
        data = {"mensaje": e}
    return JsonResponse(data)


def deduccion_tipo_actualizar(request):
    data = {}
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        id = data["id"]
        deduccion_tipo = data["deduccion_tipo"]
        es_legal = data["es_legal"]
        es_externa = data["es_externa"]
        active = data["active"]
        obj = DeduccionTipo.objects.get(pk=id)
        obj.deduccion_tipo = deduccion_tipo
        obj.es_legal = es_legal
        obj.es_externa = es_externa
        obj.active = active
        obj.save()
        data = {"mensaje": "Se ha actualizado el registro"}
    else:
        data = {"mensaje": "Método no válido"}

    return JsonResponse(data)


def deduccion_tipo_guardar(request):
    data = {}
    if request.is_ajax():
        if request.method == "POST":
            data = json.loads(request.body.decode("utf-8"))
            deduccion_tipo = data["deduccion_tipo"]
            es_legal = data["es_legal"]
            es_externa = data["es_externa"]
            indice_relevancia = data["indice_relevancia"]
            obj = DeduccionTipo(
                deduccion_tipo=deduccion_tipo,
                es_legal=es_legal,
                es_externa=es_externa,
                indice_relevancia=indice_relevancia,
                visible=True,
                active=True,
            )
            obj.save()
            data = {"mensaje": "Se ha guardado el registro", "error":False}
        else:
            data = {"mensaje": "El método no está permitido", "error":True}
    else:
        data = {"mensaje": "El tipo de petición no está permitido", "error":True}
    return JsonResponse(data)


# -------------------END AJAX -------------------
# endregion

# region Código para Deducciones Empleado

# >>>>>>>>>>>>>>>>>>>AJAX<<<<<<<<<<<<<<<<<<<<<


@login_required(login_url="/form/iniciar-sesion/")
def deduccion_empleado_listado(request):
    msj = ""
    data = {}
    lista = []
    try:
        data = DeduccionTipo.objects.all()
        for item in data:
            objeto = {
                "id": item.pk,
                "deduccion_tipo": item.deduccion_tipo,
                "es_legal": item.es_legal,
                "es_externa": item.es_externa,
                "indice_relevancia": item.indice_relevancia,
            }
            lista.append(objeto)
        data = {"mensaje": "Operación finalizada correctamente", "datos": lista}
    except Exception as e:
        data = {"mensaje": e}
    print(data)
    return JsonResponse(data)


# >>>>>>>>>>>>>>>>>>>END AJAX<<<<<<<<<<<<<<<<<

# endregion

# region Código para Ingresos Tipo


def ingresos_tipo_listado(request):
    return render(request, "ingresos_tipo.html")


# >>>>>>>>>>>>>>>>> AJAX <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


def ingresos_tipo_obtener(request):
    data = {}
    datos = []
    try:
        if request.is_ajax():
            suc = Branch.objects.get(pk=request.session["sucursal"])
            tipos = IngresoTipo.objects.filter(empresa_reg=suc.empresa)
            for item in tipos:
                obj = {
                    "id": item.pk,
                    "ingreso_tipo": item.ingreso_tipo,
                    "indice_relevancia": item.indice_relevancia,
                    "visible": item.visible,
                    "active": item.active,
                }
                datos.append(obj)
            data = {"mensaje": "¡Éxito!", "error": False, "tipos": datos}
        else:
            data = {"mensaje": "Tipo de petición no válida", "error": True}
    except Exception as e:
        data = {"mensaje": str(e)}
    return JsonResponse(data)


def ingreso_tipo_guardar(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                data = json.loads(request.body.decode("utf-8"))
                ingreso_tipo = data["ingreso_tipo"]
                indice_relevancia = data["indice_relevancia"]

                if len(ingreso_tipo) == 0:
                    data = {
                        "mensaje": 'Se pasó un valor no válido para el campo "Tipo de Ingreso".',
                        "error": True,
                    }
                    return JsonResponse(data)

                if len(indice_relevancia) == 0:
                    data = {
                        "mensaje": 'Se pasó un valor no válido para el campo "Índicie de relevancia".',
                        "error": True,
                    }
                    return JsonResponse(data)
                else:
                    if int(indice_relevancia) == 0:
                        data = {
                            "mensaje": 'Se pasó un valor no válido para el campo "Índicie de relevancia".',
                            "error": True,
                        }
                        return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])

                obj = IngresoTipo(
                    ingreso_tipo=ingreso_tipo,
                    indice_relevancia=indice_relevancia,
                    visible=True,
                    empresa_reg=suc.empresa,
                    active=True,
                )
                obj.save()
                data = {"mensaje": "Se ha guardado el registro", "error": False}
            else:
                data = {"mensaje": "El método no está permitido", "error": True}
        else:
            data = {"mensaje": "El tipo de petición no es válido", "error": True}
    except Exception as e:
        data = {"mensaje": str(e)}
    return JsonResponse(data)

def ingreso_tipo_actualizar(request):
    data = {}
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        id = data["id"]
        ingreso_tipo = data["ingreso_tipo"]
        indice = data["indice_relevancia"]
        active = data["active"]
        obj = IngresoTipo.objects.get(pk=id)
        obj.ingreso_tipo = ingreso_tipo
        obj.indice_relevancia = indice
        obj.active = active
        obj.save()
        data = {"mensaje": "Se ha actualizado el registro","error": False}
    else:
        data = {"mensaje": "Método no válido", "error": True}

    return JsonResponse(data)

def ingreso_tipo_eliminar(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                data = json.loads(request.body.decode("utf-8"))
                id = data["id"]
                if int(id) == 0:
                    data = {
                        "mensaje": "No se pasó un valor válido para el registro a eliminar.",
                        "error": True,
                    }
                else:
                    o_ingT = IngresoTipo.objects.get(pk=id)
                    o_ingT.delete()
                    data = {"mensaje": "El registro ha sido eliminado", "error": False}
            else:
                data = {"mensaje": "El método no está permitido", "error": True}
        else:
            data = {"mensaje": "El tipo de petición no está permitido", "error": True}
    except Exception as e:
        data = {"mensaje": str(e), "error": True}
    return JsonResponse(data)


def ingreso_tipo_obtener(request):
    data = {}
    try:
        id = request.GET.get("id")
        obj = IngresoTipo.objects.get(pk=id)
        data = {
            "id": obj.pk,
            "ingreso_tipo": obj.ingreso_tipo,
            "indice_relevancia": obj.indice_relevancia,
            "visible": obj.visible,
            "active": obj.active,
        }
    except Exception as e:
        data = {"mensaje": str(e)}
    return JsonResponse(data)


# <<<<<<<<<<<<<<<<<<<< AJAX >>>>>>>>>>>>>>>>>>>>>>>>>>>

# endregion

# region Código para Ingresos Empleado


def ingresos_empleado_listado(request):
    verificaSucursal(request)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(branch=suc, active=True).order_by("firstName")
    planillas = Planilla.objects.filter(cerrada=False, sucursal_reg=suc, active=True)
    planillas_l = Planilla.objects.filter(sucursal_reg=suc, active=True)
    tipo_ingresos = IngresoTipo.objects.filter(active=True, visible=True)
    return render(
        request,
        "ingresos-empleado.html",
        {"empleados": empleados, "planillas": planillas, "planillas_l": planillas_l, "ingresos": tipo_ingresos},
    )


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>> AJAX <<<<<<<<<<<<<<<<<<<<<<<<<<<<


def ingresos_empleados_obtener_filtro(request):
    data = {}
    datos_l = []
    q_list = []
    datos = []
    total_monto = 0
    planilla = request.GET.get("planilla")
    empleado = request.GET.get("empleado")
    ingreso = request.GET.get("ingreso")

    if len(empleado) > 0:
        if int(empleado) > 0:
            q_list.append(Q(empleado__pk=empleado))

    if len(planilla) > 0:
        if int(planilla) > 0:
            q_list.append(Q(planilla__pk=planilla))

    if len(ingreso) > 0:
        if int(ingreso) > 0:
            q_list.append(Q(ingreso__pk=ingreso))

    if len(q_list) > 0:
        datos = IngresoEmpleado.objects.filter(functools.reduce(operator.and_, q_list))

    for item in datos:
        empleado = item.empleado.firstName
        if item.empleado.middleName:
            empleado += " " + item.empleado.middleName
        empleado += " " + item.empleado.lastName
        obj = {
            "id": item.pk,
            "empleado": empleado,
            "codigo": item.empleado.extEmpNo,
            "ingreso": item.ingreso.ingreso_tipo,
            "monto": formato_millar(item.monto),
            "active": item.active,
        }
        datos_l.append(obj)
        total_monto += item.monto
    data = {"datos": datos_l, "total": formato_millar(total_monto)}
    return JsonResponse(data)

def ingresos_empleados_guardar(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                data = json.loads(request.body.decode("utf-8"))
                planilla_id = data["planilla"]
                empleado_id = data["empleado"]
                ingreso_id = data["ingreso"]
                monto = data["monto"]

                if int(planilla_id) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Planilla"',
                        "error": True,
                    }

                if int(ingreso_id) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Ingreso"',
                        "error": True,
                    }

                if int(empleado_id) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Empleado"',
                        "error": True,
                    }

                if len(monto) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Monto"',
                        "error": True,
                    }
                else:
                    if float(monto) == 0:
                        data = {
                            "mensaje": 'No se ha pasado un valor válido para el campo "Monto"',
                            "error": True,
                        }

                o_planilla = Planilla.objects.get(pk=planilla_id)
                o_ingreso = IngresoTipo.objects.get(pk=ingreso_id)
                o_empleado = Employee.objects.get(pk=empleado_id)
                suc = Branch.objects.get(pk=request.session["sucursal"])

                cons = IngresoEmpleado.objects.filter(
                    planilla=o_planilla, empleado=o_empleado, ingreso=o_ingreso
                )
                if cons.exists():
                    data = {
                        "mensaje": "Ya existe el ingreso para el empleado en la planilla seleccionada.",
                        "error": True,
                    }
                else:
                    o_bj = IngresoEmpleado(
                        planilla=o_planilla,
                        ingreso=o_ingreso,
                        empleado=o_empleado,
                        monto=monto,
                        empresa_reg=suc.empresa,
                        user_reg=request.user,
                    )
                    o_bj.save()
                    data = {"mensaje": "Se ha creado el registro.", "error": False}
            else:
                data = {"mensaje": "El método no está permitido", "error": True}
        else:
            data = {
                "mensaje": "El tipo de petición http no está permitido",
                "error": True,
            }
    except Exception as e:
        data = {"mensaje": str(e), "error": True}
    return JsonResponse(data)

def ingresos_empleados_eliminar(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                data = json.loads(request.body.decode("utf-8"))
                ded_id = data["id"]
                if int(ded_id) == 0:
                    data = {
                        "mensaje": "No se pasó un valor válido para el registro a eliminar.",
                        "error": True,
                    }
                else:
                    o_ded = IngresoEmpleado.objects.get(pk=ded_id)
                    o_ded.delete()
                    data = {"mensaje": "El registro ha sido eliminado", "error": False}
            else:
                data = {"mensaje": "El método no está permitido", "error": True}
        else:
            data = {"mensaje": "El tipo de petición no está permitido", "error": True}
    except Exception as e:
        data = {"mensaje": str(e), "error": True}
    return JsonResponse(data)

def ingresos_reversion(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                data = json.loads(request.body.decode("utf-8"))
                planilla_id = data['planilla']
                ingreso_id = data['ingreso']
                if int(planilla_id) == 0:
                    data = {
                        "mensaje": "No se pasó un valor válido en el campo 'Planilla'",
                        "error": True,
                    }
                else:
                    o_planilla = Planilla.objects.get(pk=planilla_id)
                    if int(ingreso_id) == 0:
                        ingresos_detalle = PlanillaDetalleIngresos.objects.filter(planilla=o_planilla)
                        ingresos = IngresoEmpleado.objects.filter(planilla=o_planilla)
                    else:
                        o_tipoingreso = IngresoTipo.objects.get(pk=ingreso_id)
                        ingresos_detalle = PlanillaDetalleIngresos.objects.filter(planilla=o_planilla, tipo_ingreso=o_tipoingreso)
                        ingresos = IngresoEmpleado.objects.filter(planilla=o_planilla, ingreso=o_tipoingreso)
                    if ingresos_detalle:
                        ingresos_detalle.delete()
                    if ingresos:
                        ingresos.delete()
                    data = {
                        "mensaje": "Se han revertido los datos",
                        "error": False,
                    }
            else:
                data = {"mensaje": "El método no está permitido", "error": True}
        else:
            data = {"mensaje": "El tipo de petición no está permitido", "error": True}
    except Exception as e:
        data = {"mensaje": str(e), "error": True}
    return JsonResponse(data)

def ingresos_empleados_obtener(request):
    data = {}
    try:
        id = request.GET.get("id")
        obj = IngresoEmpleado.objects.get(pk=id)
        obj_V = {
            "id": obj.pk,
            "empleado": obj.empleado.id,
            "planilla": obj.planilla.id,
            "deduccion": obj.ingreso.id,
            "monto": obj.monto,
            "active": obj.active,
        }
        data = {"mensaje": "Exito", "error": False, "dato": obj_V}
    except Exception as e:
        data = {"mensaje": str(e), "error": True}
    return JsonResponse(data)

def ingresos_empleados_actualizar(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                data = json.loads(request.body.decode("utf-8"))
                id = data["id"]
                monto = data["monto"]
                active = data["active"]

                if len(monto) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Monto"',
                        "error": True,
                    }
                else:
                    if float(monto) == 0:
                        data = {
                            "mensaje": 'No se ha pasado un valor válido para el campo "Monto"',
                            "error": True,
                        }

                obj = IngresoEmpleado.objects.get(pk=id)

                obj.monto = monto
                obj.active = active
                obj.user_mod = request.user
                obj.date_mod = datetime.datetime.now()
                obj.save()
                data = {"mensaje": "Se ha actualizado el registro", "error": False}
            else:
                data = {"mensaje": "Método no permitido", "error": True}
        else:
            data = {"mensaje": "Tipo de petición no está permitido", "error": True}
    except Exception as e:
        data = {"mensaje": str(e), "error": True}
    return JsonResponse(data)

def ingresos_empleados_archivo_guardar(request):
    data = {}
    lista_bulk = []
    try:
        if request.is_ajax():
            if request.method == "POST":
                suc = Branch.objects.get(pk=request.session["sucursal"])
                planilla = request.POST["planilla"]
                ingreso = request.POST["ingreso"]
                if len(planilla) == 0 or planilla == "null":
                    data = {
                        "mensaje": "No se pasó un valor válido para el campo planilla",
                        "error": True,
                    }
                    return JsonResponse(data)
                else:
                    if int(planilla) == 0:
                        data = {
                            "mensaje": "No se pasó un valor válido para el campo planilla",
                            "error": True,
                        }
                        return JsonResponse(data)

                if len(ingreso) == 0 or ingreso == "null":
                    data = {
                        "mensaje": "No se pasó un valor válido para el campo tipo deducción",
                        "error": True,
                    }
                    return JsonResponse(data)
                else:
                    if int(ingreso) == 0:
                        data = {
                            "mensaje": "No se pasó un valor válido para el campo tipo deducción",
                            "error": True,
                        }
                        return JsonResponse(data)

                form = DeduccionEmpleadoForm(request.POST, request.FILES)
                if form.is_valid():
                    bandera = False
                    tot_reg_mod = 0
                    mensaje = ""
                    datosf = request.FILES["archivo"]
                    df = pandas.read_excel(
                        datosf, sheet_name="Ingresos", usecols=["Codigo", "Monto"]
                    )
                    datos = df.to_dict(orient="record")
                    for item in datos:
                        codigo = item["Codigo"]
                        if Employee.objects.filter(extEmpNo=codigo).exists():
                            o_empleado = Employee.objects.get(
                                extEmpNo=codigo, active=True
                            )
                            if o_empleado.branch != suc:
                                data = {
                                    "mensaje": "El empleado con código "
                                    + str(codigo)
                                    + " no está asignado a la sucursal en sesión.",
                                    "error": True,
                                }
                                bandera = True
                            else:
                                o_planilla = Planilla.objects.get(pk=planilla)
                                o_tipo_ing = IngresoTipo.objects.get(pk=ingreso)
                                o_ing = IngresoEmpleado.objects.filter(
                                    empleado=o_empleado,
                                    planilla=o_planilla,
                                    ingreso=o_tipo_ing,
                                )
                                if o_ing.exists():
                                    o_ing = IngresoEmpleado.objects.get(
                                        empleado=o_empleado,
                                        planilla=o_planilla,
                                        ingreso=o_tipo_ing,
                                    )
                                    o_ing.monto = item["Monto"]
                                    o_ing.save()
                                    tot_reg_mod += 1
                                else:
                                    o_ded = IngresoEmpleado(
                                        empleado=o_empleado,
                                        planilla=o_planilla,
                                        ingreso=o_tipo_ing,
                                        monto=item["Monto"],
                                        empresa_reg=suc.empresa,
                                        user_reg=request.user,
                                    )
                                    if item["Monto"] > 0:
                                        lista_bulk.append(o_ded)
                        else:
                            data = {
                                "mensaje": "El empleado con código "
                                + str(codigo)
                                + " no existe.",
                                "error": True,
                            }
                            bandera = True
                        if bandera:
                            return JsonResponse(data)

                    IngresoEmpleado.objects.bulk_create(lista_bulk)
                    if len(lista_bulk) > 0:
                        mensaje = (
                            "Se han cargado " + str(len(lista_bulk)) + " registros. "
                        )
                    if tot_reg_mod > 0:
                        mensaje += (
                            "Se ha modificado " + str(tot_reg_mod) + " registros."
                        )
                    data = {"mensaje": mensaje, "error": False}
                else:
                    data = {"mensaje": "Datos incompletos", "error": True}
            else:
                data = {"mensaje": "El método no es válido.", "error": True}
        else:
            data = {"mensaje": "La petición no es asíncrona", "error": True}
    except Exception as e:
        data = {"mensaje": str(e), "error": True}

    return JsonResponse(data)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>> AJAX <<<<<<<<<<<<<<<<<<<<<<<<<<<<
# endregion

# region Código para Contratos

def contratos_page(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(branch=suc).order_by("firstName")
    tipos_contratos = TipoContrato.objects.filter(empresa_reg=suc.empresa).order_by("tipo_contrato")
    return render(request,"contratos_listado.html",{"empleados": empleados, "tipos_contrato": tipos_contratos})

# >>>>>>>>>>>>>>>>> AJAX <<<<<<<<<<<<<<<<<<<<<<<<<

def contratos_listado(request):
    data = {}
    datos = []
    contratos = []
    if request.is_ajax():
        suc = Branch.objects.get(pk=request.session["sucursal"])
        if "id" in request.GET:
            id = request.GET.get("id")
            if id == "0":
                contratos = Contrato.objects.filter(empleado__branch=suc)

            else:
                contratos = Contrato.objects.filter(empleado__pk=id, empresa_reg=suc.empresa)
        for item in contratos:
            empleado = item.empleado.firstName
            if item.empleado.middleName:
                empleado += " " + item.empleado.middleName
            empleado += " " + item.empleado.lastName
            obj = {
                "id": item.pk,
                "numero_contrato": item.numero,
                "empleado": empleado,
                "fecha_inicio": datetime.datetime.strftime(item.fecha_inicio,"%d/%m/%Y"),
                "fecha_fin": datetime.datetime.strftime(item.fecha_fin, "%d/%m/%Y"),
                "tipo_contrato": item.tipo_contrato.tipo_contrato,
                "active": item.active,
            }
            datos.append(obj)
    data = {"data": datos}
    return JsonResponse(data)

def contratos_guardar(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                data = json.loads(request.body.decode("utf-8"))
                empleado_id = data["empleado"]
                tipo_contrato_id = data["tipo_contrato"]
                fecha_inicio = data["fecha_inicio"]
                fecha_fin = data["fecha_fin"]

                if int(empleado_id) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Empleado"',
                        "error": True,
                    }
                    return JsonResponse(data)
                if int(tipo_contrato_id) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Tipo de contrato"',
                        "error": True,
                    }
                    return JsonResponse(data)
                if str(fecha_inicio) == "":
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Fecha de inicio"',
                        "error": True,
                    }
                    return JsonResponse(data)
                if str(fecha_fin) == "":
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Fecha de vencimiento"',
                        "error": True,
                    }
                    return JsonResponse(data)

                vfe1 = str(fecha_inicio)
                vfe2 = str(fecha_fin)

                fecha_inicio = datetime.datetime.strptime(vfe1, '%d/%m/%Y')
                fecha_fin = datetime.datetime.strptime(vfe2, '%d/%m/%Y')
                
                o_tipocontrato = TipoContrato.objects.get(pk=tipo_contrato_id)
                o_empleado = Employee.objects.get(pk=empleado_id)
                suc = Branch.objects.get(pk=request.session["sucursal"])

                num_contrato = my_random_string(10)
                ver = Contrato.objects.filter(numero=num_contrato)

                while ver.count() > 0:
                    num_contrato = my_random_string(10)
                    ver = Contrato.objects.filter(numero=num_contrato)

                ver = Contrato.objects.filter(numero=num_contrato)

                if ver.exists():
                    data = {
                        "mensaje": 'El numero de contrato ya existe.',
                        "error": True,
                    }
                    return JsonResponse(data)

                con = Contrato.objects.filter(
                    empleado=o_empleado,
                    tipo_contrato=o_tipocontrato,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                )
                if con.exists():
                    data = {"mensaje": "El contrato ya existe", "error": True}
                else:
                    o_contrato = Contrato(
                        numero = my_random_string(10),
                        empleado=o_empleado,
                        tipo_contrato=o_tipocontrato,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin,
                        empresa_reg=suc.empresa,
                        user_reg=request.user,
                        active=True,
                    )
                    o_contrato.save()
                    data = {"mensaje": "¡Éxito!", "error": False}
            else:
                data = {"mensaje": "El método no está permitido", "error": True}
        else:
            data = {
                "mensaje": "El tipo de petición http no está permitido",
                "error": True,
            }
    except Exception as e:
        data = {"mensaje": str(e), 'error':True}
    return JsonResponse(data)

def contrato_obtener(request):
    data = {}
    try:
        id = request.GET.get("id")
        obj = Contrato.objects.get(pk=id)
        empleado = obj.empleado.firstName
        if obj.empleado.middleName:
            empleado += " " + obj.empleado.middleName
        empleado += " " + obj.empleado.lastName
        obj_V = {
            "id": obj.pk,
            "numero": obj.numero,
            "empleado": obj.empleado.pk,
            "fecha_inicio": datetime.datetime.strftime(obj.fecha_inicio, "%d/%m/%Y"),
            "fecha_fin": datetime.datetime.strftime( obj.fecha_fin, "%d/%m/%Y"),
            "tipo_contrato": obj.tipo_contrato.pk,
            "active": obj.active,
        }
        data = {"mensaje": "Exito", "error": False, "dato": obj_V}
    except Exception as e:
        data = {"mensaje": str(e), "error": True}
    return JsonResponse(data)

def contrato_actualizar(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == "POST":
                data = json.loads(request.body.decode("utf-8"))
                id = data["id"]
                fecha_inicio = data["fecha_inicio"]
                fecha_fin = data["fecha_fin"]
                active = data["active"]

                if len(fecha_inicio) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Fecha inicio"',
                        "error": True,
                    }

                if len(fecha_fin) == 0:
                    data = {
                        "mensaje": 'No se ha pasado un valor válido para el campo "Fecha de vencimiento"',
                        "error": True,
                    }

                vfe1 = str(fecha_inicio)
                vfe2 = str(fecha_fin)

                fecha_inicio = datetime.datetime.strptime(vfe1, '%d/%m/%Y')
                fecha_fin = datetime.datetime.strptime(vfe2, '%d/%m/%Y')
                print(fecha_inicio)
                print(fecha_fin)

                obj = Contrato.objects.get(pk=id)

                obj.fecha_inicio = fecha_inicio
                obj.fecha_fin = fecha_fin
                obj.active = active
                obj.user_mod = request.user
                obj.date_mod = datetime.datetime.now()
                obj.save()
                data = {"mensaje": "Se ha actualizado el registro", "error": False}
            else:
                data = {"mensaje": "Método no permitido", "error": True}
        else:
            data = {"mensaje": "Tipo de petición no está permitido", "error": True}
    except Exception as e:
        data = {"mensaje": str(e), "error": True}
    return JsonResponse(data)

# >>>>>>>>>>>>>>>>> AJAX <<<<<<<<<<<<<<<<<<<<<<<<<
# endregion

# region Código para Impresión Boleta de Pago
def impresion_boletas(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    departamentos = Department.objects.filter(empresa_reg=suc.empresa)
    planillas = Planilla.objects.filter(sucursal_reg=suc, cerrada=True)
    context = {
        'planillas': planillas,
        'departamentos': departamentos
    }
    return render(request, "reportes/impresion_boletas.html", context)

def envio_boleta_correo(request):
    if request.method == 'POST':
        planilla_id = request.POST['cboPlanillaC']
        departamento_id = request.POST['cboDepartamentoC']
        if int(planilla_id) == 0:
            messages.add_message(request, messages.WARNING, 'El campo "Planilla" requiere un valor.')
            return redirect('impresion_boletas')
        else:
            o_planilla = Planilla.objects.get(pk=planilla_id)
            if int(departamento_id) == 0:
                detalles_planillas = PlanillaDetalle.objects.filter(planilla=o_planilla).exclude(empleado__email='')
            elif int(departamento_id) > 0:
                o_depto = Department.objects.get(pk=int(departamento_id))
                detalles_planillas = PlanillaDetalle.objects.filter(planilla=o_planilla, empleado__dept=o_depto).exclude(empleado__email='')
            for item in detalles_planillas:
                detalle_deducciones = PlanillaDetalleDeducciones.objects.filter(planilla=o_planilla, empleado=item.empleado)
                detalle_ingresos = PlanillaDetalleIngresos.objects.filter(planilla=o_planilla, empleado=item.empleado)
                boleta_pago_email_masivo(detalle_ingresos, detalle_deducciones, item.empleado, o_planilla, item)
                
            messages.add_message(request, messages.SUCCESS, 'Se enviaron los correos.')
    return redirect('impresion_boletas')
# endregion

#region Código para Reporte de Cuentas Contables
def cuentas_contables_page(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    planillas = Planilla.objects.filter(sucursal_reg=suc, active=True, cerrada=True).order_by('-fecha_pago', 'pk')
    return render(request, 'reportes/cuentas_contables.html', {"planillas": planillas})

#--------------------------->>> AJAX <<<<--------------------

def cuentas_contables_generar(request):
    try:
        datos = []
        total = 0
        if not request.user.is_anonymous():
            planilla_id = request.GET.get("planilla_id")
            planilla_obj = Planilla.objects.get(pk=planilla_id)
            detalle = PlanillaDetalle.objects.filter(planilla=planilla_obj).values('empleado__dept__description').annotate(Sum("total_ingresos"), Sum("total_deducciones"))
            for item in detalle:
                objeto = {
                    'departamento': item["empleado__dept__description"],
                    'total': formato_millar(item["total_ingresos__sum"] - item["total_deducciones__sum"])
                }
                datos.append(objeto)
                total += (item["total_ingresos__sum"] - item["total_deducciones__sum"])
            data = {
                "mensaje": None,
                "datos": datos,
                "total": formato_millar(total)
            }
        else:
            data = {
                "mensaje": "El tipo de petición no está permitida",
            }
        return JsonResponse(data)
    except Exception as ex:
        return JsonResponse({"mensaje": str(ex)})

#endregion

def verifica_saldo_controlado(request):
    try:
        if request.is_ajax():
            id = request.GET.get("id")
            id = int(id)
            if DeduccionIndividual.objects.filter(pk=id).exists():
                o_ded = DeduccionIndividual.objects.get(pk=id)
                data = {
                    "status": True,
                    "controla_saldo": o_ded.control_saldo,
                    "mensaje": "¡OK!",
                }
                return JsonResponse(data, status=200)
            else:
                data = {"status": False, "mensaje": "El tipo de petición no es válido"}
                return JsonResponse(data, status=404)
        else:
            data = {"status": False, "mensaje": "El tipo de petición no es válido"}
            return JsonResponse(data, status=404)
    except Exception as ex:
        data = {"status": False, "mensaje": str(ex)}
        return JsonResponse(data, status=500)


def obtener_fecha_limite(request):
    fecha_limite = None
    if request.is_ajax():
        id_empleado = request.GET.get("empleado")
        cuota = request.GET.get("cuotas")
        fecha_inicial = request.GET.get("fecha_inicial")
        if len(id_empleado) == 0:
            data = {"error": True, "msj": "Valor inválido de empleado"}
            return JsonResponse(data)

        if not validarEntero(id_empleado):
            data = {"error": True, "msj": "Valor inválido de empleado"}
            return JsonResponse(data)

        if not Employee.objects.filter(pk=id_empleado).exists():
            data = {"error": True, "msj": "Valor inválido de empleado"}
            return JsonResponse(data)

        if not cuota:
            data = {"error": True, "msj": "Valor no válido como cantidad de cuotas."}
            return JsonResponse(data)

        if len(cuota) == 0:
            data = {"error": True, "msj": "Valor no válido como cantidad de cuotas."}
            return JsonResponse(data)

        if not validarEntero(cuota):
            data = {"error": True, "msj": "Valor no válido como cantidad de cuotas"}
            return JsonResponse(data)

        if int(cuota) == 0:
            data = {"error": True, "msj": "Valor no válido como cantidad de cuotas"}
            return JsonResponse(data)

        if len(fecha_inicial) == 0:
            data = {"error": True, "msj": "Valor no válido como fecha inicial"}
            return JsonResponse(data)

        o_empleado = Employee.objects.get(pk=id_empleado)

        if not o_empleado.salaryUnits:
            if len(fecha_inicial) == 0:
                data = {
                    "error": True,
                    "msj": "Empleado no tiene asignado frecuencia de pago",
                }
                return JsonResponse(data)

        dias_t = int(o_empleado.salaryUnits.dias_salario) * int(cuota)
        print(dias_t)
        fecha_inicial = datetime.datetime.strptime(fecha_inicial, "%d/%m/%Y")
        fecha_limite = fecha_inicial + dtiempo.timedelta(days=dias_t)
        fecha_limite = datetime.datetime.strftime(fecha_limite, "%d/%m/%Y")
        data = {"error": False, "fecha": fecha_limite}
        return JsonResponse(data)
    else:
        data = {"error": True, "msj": "Método no permitido"}
        return JsonResponse(data)


# --------------------------VALIDACIONES------------------------------


def validarEntero(dato):
    try:
        dato = int(dato)
        dato += 1
        dato = dato / 1
        return True
    except Exception:
        return False


def validarDecimal(dato):
    try:
        dato = float(dato)
        return True
    except TypeError:
        return False


def formato_millar(valor):
    if valor:
        return locale.format("%.2f", valor, grouping=True)
    else:
        if valor == 0:
            return locale.format("%.2f", valor, grouping=True)
        return None

def resp_serv(error, mensaje):
    return {'error': error, 'mensaje': mensaje}
# region Reportes


def reporte_empleados(request):
    if not "sucursal" in request.session:
        return HttpResponseRedirect("/salir/")
    else:
        if int(request.session["sucursal"]) < 1:
            return HttpResponseRedirect("/salir/")
    suc = Branch.objects.get(pk=request.session["sucursal"])
    departamentos = Department.objects.filter(active=True, empresa_reg=suc.empresa)
    tipos_contratos = TipoContrato.objects.filter(active=True, empresa_reg=suc.empresa)
    tipos_nominas = TipoNomina.objects.filter(active=True, empresa_reg=suc.empresa)
    empleados = Employee.objects.filter(active=True, branch=suc)
    return render(
        request,
        "reportes/reporte-empleado1.html",
        {
            "empleados": empleados,
            "departamentos": departamentos,
            "tipos_contratos": tipos_contratos,
            "tipos_nominas": tipos_nominas,
        },
    )


def obtener_depto_empleados(request):
    datos = []
    data = {}
    sum_tot_sal = 0
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.is_ajax():
        deptos = Employee.objects.filter(branch=suc, active=True).values('dept__pk', 'dept__code', 'dept__description').order_by('dept__description').distinct()
        #deptos = Department.objects.filter(empresa_reg=suc.empresa, active=True)
        
        for departamento in deptos:
            tot_emp = 0
            tot_sal = 0
            # if departamento["dept__pk"]:
            #     pass
            filas = Employee.objects.filter(dept__pk=departamento["dept__pk"], active=True, branch=suc)
            tot_emp = filas.count()
            for fila in filas:
                if fila.salary:
                    tot_sal += float(fila.salary)
                    sum_tot_sal += float(fila.salary)
                    
            o_depto = {
                "id": departamento["dept__pk"] if   departamento["dept__pk"] else 0,
                "codigo": departamento["dept__code"] if departamento["dept__code"] else "--",
                "descripcion": departamento["dept__description"] if  departamento["dept__description"] else "--",
                "total_empleados": tot_emp,
                "total_salarios": formato_millar(tot_sal),
            }
            datos.append(o_depto)
    else:
        pass
    data = {'data': datos, 'suma_salarios': formato_millar(sum_tot_sal)}
    return JsonResponse(data)
    #return render(request, "reportes/ajax/depto-empleados.html", {"datos": datos, "suma_salarios": formato_millar(sum_tot_sal)})

def obtener_empleados_depto(request):
    data = {}
    datos = []
    l_datos = []
    tot_salarios = 0
    try:
        if request.is_ajax():
            id = request.GET.get('id')
            suc = Branch.objects.get(pk=request.session["sucursal"])
            id = int(id)
            if id == 0:
                datos = Employee.objects.filter(active=True, branch=suc, dept=None).order_by('firstName')
            elif id > 0:
                depto = Department.objects.get(pk=id)
                datos = Employee.objects.filter(active=True, branch=suc, dept=depto).order_by('firstName')
            for item in datos:
                nombre = item.firstName
                if item.middleName:
                    nombre += " " + item.middleName
                nombre += " " + item.lastName
                obj = {
                    'id': item.pk,
                    'codigo': item.extEmpNo,
                    'nombre': nombre,
                    'salario': formato_millar(float(item.salary)),
                }
                l_datos.append(obj)
                tot_salarios += float(item.salary)
            tot_salarios = formato_millar(tot_salarios)
            data = {'error':False, 'mensaje': '¡Éxito!', 'datos': l_datos, 'total_salarios': tot_salarios}
        else:
            data = resp_serv(True, 'Acción no permitida.')
    except Exception as ex:
        data = resp_serv(True, str(ex))
    return JsonResponse(data)

def obtener_deptos_empleados_excel(request):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    for row_num, columns in enumerate(data):
        for col_num, cell_data in enumerate(columns):
            worksheet.write(row_num, col_num, cell_data)

    workbook.close()
    output.seek(0)

    filename = 'django_simple.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

def my_random_string(string_length=10):
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace("-","")
    return random[0:string_length]


# endregion


class Pdf(View):
    def get(self, request):
        params = {}
        empleado_id = request.GET.get("empleado_id")
        planilla_id = request.GET.get("planilla_id")
        detalle_ing = []
        detalle_ded = []
        empleado_id = int(empleado_id)
        o_empleado = Employee.objects.get(pk=empleado_id)
        o_planilla = Planilla.objects.get(pk=planilla_id)
        o_pla_de_ing = PlanillaDetalleIngresos.objects.filter(
            empleado=o_empleado, planilla=o_planilla
        ).order_by('tipo_ingreso__indice_relevancia')
        o_pla_de_ded = (
            PlanillaDetalleDeducciones.objects.filter(
                empleado=o_empleado, planilla=o_planilla
            ).order_by('tipo_deduccion__indice_relevancia')
            #.values("deduccion")
            #.annotate(Sum("valor"))
        )
        print(o_pla_de_ded)
        o_pla_de = PlanillaDetalle.objects.get(empleado=o_empleado, planilla=o_planilla)
        for item in o_pla_de_ing:
            vingres = ""
            vparam = "SALARIO"
            vingres = item.ingreso
            data = {"ingreso": item.ingreso, "valor": formato_millar(item.valor)}
            if vingres.strip() == vparam:
                detalle_ing.append(data)

        for item in o_pla_de_ing:
            vingres = ""
            vparam = "SALARIO"
            vingres = item.ingreso
            data = {"ingreso": item.ingreso, "valor": formato_millar(item.valor)}
            if vingres.strip() != vparam:
                detalle_ing.append(data)

        for item in o_pla_de_ded:
            data = {
                "deduccion": item.deduccion,
                "valor": formato_millar(item.valor),
            }
            detalle_ded.append(data)
        params = {
            "empleado": o_empleado,
            "planilla": o_planilla,
            "dias_laborados": int(o_pla_de.dias_salario)
            - int(o_pla_de.dias_ausentes_sin_pago),
            "ingresos": detalle_ing,
            "deducciones": detalle_ded,
            "total_ingresos": formato_millar(o_pla_de.total_ingresos),
            "total_deducciones": formato_millar(o_pla_de.total_deducciones),
            "salario_neto": formato_millar(
                o_pla_de.total_ingresos - o_pla_de.total_deducciones
            ),
            "request": request,
        }
        return Render.render("reportes/reporte_boleta.html", params)

class ReportePlanillaSeleccion(View):
    def get(self, request):
        params = {}
        registros = []
        footer = []
        q_list = []
        planilla_id = request.GET.get("cboPlanilla")
        formato = request.GET.get("cboFormato")
        o_planilla = Planilla.objects.get(pk=planilla_id)

        columnas = [{"title": "Codigo"}, {"title": "Nombre"}, {"title": "Departamento"}]
        tipos_ingresos = IngresoTipo.objects.values('ingreso_tipo', 'pk').order_by('indice_relevancia')
        for item in tipos_ingresos:
            obj = {
                'title': item["ingreso_tipo"],
            }
            columnas.append(obj)

        columnas.append({'title':'Total Ingreso'})
    
        tipos_deduciones = DeduccionTipo.objects.values('deduccion_tipo', 'pk').order_by('indice_relevancia')
        for item1 in tipos_deduciones:
            obj = {
                'title': item1['deduccion_tipo'],
            }
            columnas.append(obj)

        columnas.append({'title':'Total Deducciones'})
        columnas.append({'title':'Total Neto'})

        empleados = PlanillaDetalleIngresos.objects.filter(planilla=o_planilla).values('empleado__pk', 'empleado__extEmpNo','empleado__firstName', 'empleado__middleName', 'empleado__lastName', 'empleado__dept__description').order_by('empleado__firstName').distinct()

        for empleado in empleados:
            ing_sum = 0
            r_ingresos = []
            r_deducciones = []
            for item in tipos_ingresos:
                ing_tot = 0
                ingresos = PlanillaDetalleIngresos.objects.filter(empleado__pk=empleado["empleado__pk"], tipo_ingreso__pk=item["pk"], planilla=o_planilla).values('ingreso', 'valor').order_by('tipo_ingreso__indice_relevancia')
                for fila in ingresos:
                    ing_tot += fila["valor"]
                    ing_sum += fila["valor"]
                obj_i = {
                    'valor': formato_millar(ing_tot)
                }
                r_ingresos.append(obj_i)
            
            #deducciones
            ded_sum = 0
            for item in tipos_deduciones:
                ded_tot = 0
                deducciones = PlanillaDetalleDeducciones.objects.filter(empleado__pk=empleado["empleado__pk"], tipo_deduccion__pk=item["pk"], planilla=o_planilla).values('deduccion', 'valor').order_by('tipo_deduccion__indice_relevancia')
                for fila in deducciones:
                    ded_tot += fila["valor"]
                    ded_sum += fila["valor"]
                obj_d = {
                    'valor': formato_millar(ded_tot)
                }
                r_deducciones.append(obj_d)

            obj = {
                "codigo": empleado["empleado__extEmpNo"],
                "nombre": empleado["empleado__firstName"] + " " + empleado["empleado__lastName"],
                "departamento": empleado["empleado__dept__description"],
                "ingresos": r_ingresos,
                "deducciones": r_deducciones,
                "total_ingresos": formato_millar(ing_sum),
                "total_deducciones": formato_millar(ded_sum),
                "total_neto": formato_millar(ing_sum-ded_sum)
            }
            registros.append(obj)

        sub_tot_ing = 0
        for item in tipos_ingresos:
            filtro_v = []
            for f_l in q_list:
                filtro_v.append(f_l)
            filtro_v.append(Q(tipo_ingreso__pk=item["pk"]))
            #sum_ing_tip = PlanillaDetalleIngresos.objects.filter(tipo_ingreso__pk=item["pk"], planilla__fecha_inicio__range=(vdesde, vhasta), planilla__fecha_fin__range=(vdesde, vhasta)).order_by('tipo_ingreso__indice_relevancia').aggregate(Sum('valor'))
            sum_ing_tip = PlanillaDetalleIngresos.objects.filter(planilla=o_planilla, tipo_ingreso__pk=item["pk"]).order_by('tipo_ingreso__indice_relevancia').aggregate(Sum('valor'))
            if sum_ing_tip["valor__sum"]:
                v_Valor = sum_ing_tip["valor__sum"]
                sub_tot_ing += sum_ing_tip["valor__sum"]
            else:
                v_Valor = 0

            obj_f = {
                "valor": formato_millar(v_Valor)
            }
            footer.append(obj_f)

        obj_f = {
            "valor": formato_millar(sub_tot_ing)
        }
        footer.append(obj_f)

        sub_tot_ded = 0
        
        for item in tipos_deduciones:
            filtro_v = []
            for f_l in q_list:
                filtro_v.append(f_l)
            filtro_v.append(Q(tipo_deduccion__pk=item["pk"]))
            #sum_ded_tip = PlanillaDetalleDeducciones.objects.filter(tipo_deduccion__pk=item["pk"], planilla__fecha_inicio__range=(vdesde, vhasta), planilla__fecha_fin__range=(vdesde, vhasta)).order_by('tipo_deduccion__indice_relevancia').aggregate(Sum('valor'))
            sum_ded_tip = PlanillaDetalleDeducciones.objects.filter(planilla=o_planilla, tipo_deduccion__pk=item["pk"]).order_by('tipo_deduccion__indice_relevancia').aggregate(Sum('valor'))

            if sum_ded_tip["valor__sum"]:
                v_Valor = sum_ded_tip["valor__sum"]
            else:
                v_Valor = 0

            obj_f = {
                "valor": formato_millar(v_Valor)
            }
            
            if sum_ded_tip["valor__sum"]:
                sub_tot_ded += sum_ded_tip["valor__sum"]
            footer.append(obj_f)

        obj_f = {
            "valor": formato_millar(sub_tot_ded),
        }
        footer.append(obj_f)
        obj_f = {
            "valor": formato_millar(sub_tot_ing-sub_tot_ded)
        }
        footer.append(obj_f)

        params = {
            "columnas":columnas,
            "desde":o_planilla.fecha_inicio,
            "hasta":o_planilla.fecha_fin,
            "empleados": registros,
            "footer": footer,
            "request": request,
        }

        if formato == "1":
            return Render.render("reportes/planilla_reporte.html", params)
        else:
            output = BytesIO()

            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet()

            archivo_imagen = settings.MEDIA_ROOT+'\imagenes\promaco-logo.png'

            worksheet.insert_image('B2', archivo_imagen)
            worksheet.write(5, 1, "REPORTE DE PLANILLA")
            worksheet.write(6, 1, "Desde: " + str(o_planilla.fecha_inicio))
            worksheet.write(7, 1, "Hasta: " + str(o_planilla.fecha_fin))

            rows = 9
            columns = 0
            for columna in params["columnas"]:                
                worksheet.write(rows, columns, columna["title"])
                columns += 1

            for registro in params["empleados"]:
                columns = 0
                rows += 1
                worksheet.write(rows, columns, registro["codigo"])
                columns += 1
                worksheet.write(rows, columns, registro["nombre"])
                columns += 1
                worksheet.write(rows, columns, registro["departamento"])
                for ingreso in registro["ingresos"]:
                    columns += 1
                    valor = ingreso["valor"].replace(',', '')
                    worksheet.write_number(rows, columns, float(valor))
                columns += 1
                valor = registro["total_ingresos"].replace(',', '')
                worksheet.write_number(rows, columns, float(valor))
                for deduccion in registro["deducciones"]:
                    columns += 1
                    valor = deduccion["valor"].replace(',', '')
                    worksheet.write_number(rows, columns, float(valor))
                columns += 1
                valor = registro["total_deducciones"].replace(',', '')
                worksheet.write_number(rows, columns, float(valor))
                columns += 1
                valor = registro["total_neto"].replace(',', '')
                worksheet.write_number(rows, columns, float(valor))

            columns = 2                
            filas_v = rows + 2
            worksheet.merge_range('A'+ str(filas_v) + ":" + "C" + str(filas_v), "Total")
            rows += 1
            for foot in params["footer"]:
                columns += 1
                valor = foot["valor"].replace(',', '')
                worksheet.write(rows, columns, float(valor))

            
            workbook.close()
            output.seek(0)

            nombre_archivo = "Planilla " + str(o_planilla.fecha_inicio) +"_" + str(o_planilla.fecha_fin) + ".xlsx"

            filename = nombre_archivo
            response = HttpResponse(
                output,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename

            return response

class ReportePlanilla(View):
    def get(self, request):
        params = {}
        registros = []
        footer = []
        q_list = []

        formato = request.GET.get("cboFormato")
        departamento_id = request.GET.get("cboDepartamento")
        tipo_contrato_id = request.GET.get("cboTipoContrato")
        tipo_planilla_id = request.GET.get("cboTipoPlanilla")
        frecuencia_pago_id = request.GET.get("cboFrecuenciaPago")
        estado_contrato = request.GET.get("cboEstadoContrato")
        sucursal_id = request.GET.get("cboSucursal")

        fecha_desde = request.GET.get("txtDesde")
        fecha_hasta = request.GET.get("txtHasta")

        if len(fecha_desde) == 0:
            data = {"error": True, "mensaje": "Seleccione un rango de fecha válido"}
            return render(request, "reportes/reporte-planilla-general.html", data)

        if len(fecha_hasta) == 0:
            data = {"error": True, "mensaje": "Seleccione un rango de fecha válido"}
            return render(request, "reportes/reporte-planilla-general.html", data)
        vdesde = datetime.datetime.strptime(fecha_desde, "%d/%m/%Y").date()
        vhasta = datetime.datetime.strptime(fecha_hasta, "%d/%m/%Y").date()
        vdesde = datetime.datetime.strftime(vdesde, "%Y-%m-%d")
        vhasta = datetime.datetime.strftime(vhasta, "%Y-%m-%d")

        if estado_contrato == "2":
            q_list.append(Q(planilla__cerrada=True))
        elif estado_contrato == "1":
            q_list.append(Q(planilla__cerrada=False))

        if int(sucursal_id) > 0:
            q_list.append(Q(empleado__branch__pk=sucursal_id))
        #q_list.append(Q(planilla__fecha_inicio__gte=desde, planilla__fecha_fin__lte=hasta))
        q_list.append(Q(planilla__fecha_inicio__range=(vdesde, vhasta), planilla__fecha_fin__range=(vdesde, vhasta)))

        if int(departamento_id) > 0:
            tot_reg = Department.objects.filter(pk=departamento_id).count()
            if tot_reg > 0:
                o_departamento = Department.objects.get(pk=departamento_id)
                if o_departamento:
                    q_list.append(Q(empleado__dept=o_departamento))

        if int(tipo_contrato_id) > 0:
            tot_reg = TipoContrato.objects.filter(pk=tipo_contrato_id).count()
            if tot_reg > 0:
                o_tipo_contrato = TipoContrato.objects.filter(pk=tipo_contrato_id)
                if o_tipo_contrato:
                    q_list.append(Q(empleado__tipo_contrato=o_tipo_contrato))

        if int(tipo_planilla_id) > 0:
            tot_reg = TipoNomina.objects.filter(pk=tipo_planilla_id).count()
            if tot_reg > 0:
                o_tipo_planilla = TipoNomina.objects.get(pk=tipo_planilla_id)
                if o_tipo_planilla:
                    q_list.append(Q(empleado__tipo_nomina=o_tipo_planilla))

        if int(frecuencia_pago_id) > 0:
            tot_reg = SalaryUnit.objects.filter(pk=frecuencia_pago_id).count()
            if tot_reg > 0:
                o_frecuencia_pago = SalaryUnit.objects.get(pk=frecuencia_pago_id)
                if o_frecuencia_pago:
                    q_list.append(Q(empleado__salaryUnits=o_frecuencia_pago))

        # if "excluir_pe" in request.GET:
        #     pass
        # else:
        #     q_list.append(Q(planilla__especial=True))

        suc = Branch.objects.get(pk=request.session["sucursal"])

        columnas = [{"title": "Codigo"}, {"title": "Nombre"}, {"title": "Departamento"}]
        tipos_ingresos = IngresoTipo.objects.values('ingreso_tipo', 'pk').order_by('indice_relevancia')
        for item in tipos_ingresos:
            obj = {
                'title': item["ingreso_tipo"],
            }
            columnas.append(obj)

        columnas.append({'title':'Total Ingreso'})
    
        tipos_deduciones = DeduccionTipo.objects.values('deduccion_tipo', 'pk').order_by('indice_relevancia')
        for item1 in tipos_deduciones:
            obj = {
                'title': item1['deduccion_tipo'],
            }
            columnas.append(obj)

        columnas.append({'title':'Total Deducciones'})
        columnas.append({'title':'Total Neto'})
        #empleados = PlanillaDetalleIngresos.objects.filter(Q(planilla__fecha_inicio__gte=vdesde, planilla__fecha_fin__lte=vhasta)).exclude(tipo_ingreso=None).values('empleado__pk', 'empleado__firstName').order_by('empleado__firstName').distinct()

        # .filter(
        #         functools.reduce(operator.and_, q_list)
        #     )

        #empleados = PlanillaDetalleIngresos.objects.filter(planilla__fecha_inicio__range=(vdesde, vhasta), planilla__fecha_fin__range=(vdesde, vhasta)).values('empleado__pk', 'empleado__extEmpNo','empleado__firstName', 'empleado__middleName', 'empleado__lastName', 'empleado__dept__description').order_by('empleado__firstName').distinct()
        empleados = PlanillaDetalleIngresos.objects.filter(functools.reduce(operator.and_, q_list)).values('empleado__pk', 'empleado__extEmpNo','empleado__firstName', 'empleado__middleName', 'empleado__lastName', 'empleado__dept__description').order_by('empleado__firstName').distinct()

        for empleado in empleados:
            ing_sum = 0
            r_ingresos = []
            r_deducciones = []
            for item in tipos_ingresos:
                ing_tot = 0
                if "excluir_pe" in request.GET:
                    ingresos = PlanillaDetalleIngresos.objects.filter(empleado__pk=empleado["empleado__pk"], tipo_ingreso__pk=item["pk"], planilla__fecha_inicio__range=(vdesde, vhasta), planilla__fecha_fin__range=(vdesde, vhasta)).exclude(planilla__especial=True).values('ingreso', 'valor').order_by('tipo_ingreso__indice_relevancia')
                else:
                    ingresos = PlanillaDetalleIngresos.objects.filter(empleado__pk=empleado["empleado__pk"], tipo_ingreso__pk=item["pk"], planilla__fecha_inicio__range=(vdesde, vhasta), planilla__fecha_fin__range=(vdesde, vhasta)).values('ingreso', 'valor').order_by('tipo_ingreso__indice_relevancia')
                for fila in ingresos:
                    ing_tot += fila["valor"]
                    ing_sum += fila["valor"]
                obj_i = {
                    'valor': formato_millar(ing_tot)
                }
                r_ingresos.append(obj_i)
            
            #deducciones
            ded_sum = 0
            for item in tipos_deduciones:
                ded_tot = 0
                if "excluir_pe" in request.GET:
                    deducciones = PlanillaDetalleDeducciones.objects.filter(empleado__pk=empleado["empleado__pk"], tipo_deduccion__pk=item["pk"], planilla__fecha_inicio__range=(vdesde, vhasta), planilla__fecha_fin__range=(vdesde, vhasta)).exclude(planilla__especial=True).values('deduccion', 'valor').order_by('tipo_deduccion__indice_relevancia')
                else:
                    deducciones = PlanillaDetalleDeducciones.objects.filter(empleado__pk=empleado["empleado__pk"], tipo_deduccion__pk=item["pk"], planilla__fecha_inicio__range=(vdesde, vhasta), planilla__fecha_fin__range=(vdesde, vhasta)).values('deduccion', 'valor').order_by('tipo_deduccion__indice_relevancia')
                for fila in deducciones:
                    ded_tot += fila["valor"]
                    ded_sum += fila["valor"]
                obj_d = {
                    'valor': formato_millar(ded_tot)
                }
                r_deducciones.append(obj_d)
            
            empleadov = empleado["empleado__firstName"]
            if empleado["empleado__middleName"]:
                empleadov += " " + empleado["empleado__middleName"]
            empleadov += " " + empleado["empleado__lastName"]

            obj = {
                "codigo": empleado["empleado__extEmpNo"],
                "nombre": empleadov,
                "departamento": empleado["empleado__dept__description"],
                "ingresos": r_ingresos,
                "deducciones": r_deducciones,
                "total_ingresos": formato_millar(ing_sum),
                "total_deducciones": formato_millar(ded_sum),
                "total_neto": formato_millar(ing_sum-ded_sum)
            }
            registros.append(obj)

        
        sub_tot_ing = 0
        for item in tipos_ingresos:
            filtro_v = []
            for f_l in q_list:
                filtro_v.append(f_l)
            filtro_v.append(Q(tipo_ingreso__pk=item["pk"]))
            if "excluir_pe" in request.GET:
                sum_ing_tip = PlanillaDetalleIngresos.objects.filter(functools.reduce(operator.and_, filtro_v)).exclude(planilla__especial=True).order_by('tipo_ingreso__indice_relevancia').aggregate(Sum('valor'))
            else:
                sum_ing_tip = PlanillaDetalleIngresos.objects.filter(functools.reduce(operator.and_, filtro_v)).order_by('tipo_ingreso__indice_relevancia').aggregate(Sum('valor'))

            #sum_ing_tip = PlanillaDetalleIngresos.objects.filter(tipo_ingreso__pk=item["pk"], planilla__fecha_inicio__range=(vdesde, vhasta), planilla__fecha_fin__range=(vdesde, vhasta)).order_by('tipo_ingreso__indice_relevancia').aggregate(Sum('valor'))
            if sum_ing_tip["valor__sum"]:
                v_Valor = sum_ing_tip["valor__sum"]
                sub_tot_ing += sum_ing_tip["valor__sum"]
            else:
                v_Valor = 0

            obj_f = {
                "valor": formato_millar(v_Valor)
            }
            footer.append(obj_f)

        obj_f = {
            "valor": formato_millar(sub_tot_ing)
        }
        footer.append(obj_f)

        sub_tot_ded = 0
        
        for item in tipos_deduciones:
            filtro_v = []
            for f_l in q_list:
                filtro_v.append(f_l)
            filtro_v.append(Q(tipo_deduccion__pk=item["pk"]))
            if "excluir_pe" in request.GET:
                sum_ded_tip = PlanillaDetalleDeducciones.objects.filter(functools.reduce(operator.and_, filtro_v)).exclude(planilla__especial=True).order_by('tipo_deduccion__indice_relevancia').aggregate(Sum('valor'))
            else:
                sum_ded_tip = PlanillaDetalleDeducciones.objects.filter(functools.reduce(operator.and_, filtro_v)).order_by('tipo_deduccion__indice_relevancia').aggregate(Sum('valor'))
            #sum_ded_tip = PlanillaDetalleDeducciones.objects.filter(tipo_deduccion__pk=item["pk"], planilla__fecha_inicio__range=(vdesde, vhasta), planilla__fecha_fin__range=(vdesde, vhasta)).order_by('tipo_deduccion__indice_relevancia').aggregate(Sum('valor'))
            

            if sum_ded_tip["valor__sum"]:
                v_Valor = sum_ded_tip["valor__sum"]
            else:
                v_Valor = 0

            obj_f = {
                "valor": formato_millar(v_Valor)
            }
            
            if sum_ded_tip["valor__sum"]:
                sub_tot_ded += sum_ded_tip["valor__sum"]
            footer.append(obj_f)

        obj_f = {
            "valor": formato_millar(sub_tot_ded),
        }
        footer.append(obj_f)
        obj_f = {
            "valor": formato_millar(sub_tot_ing-sub_tot_ded)
        }
        footer.append(obj_f)

        params = {
            "columnas":columnas,
            "desde":fecha_desde,
            "hasta":fecha_hasta,
            "empleados": registros,
            "footer": footer,
            "request": request,
        }
        if formato == "1":
            return Render.render("reportes/planilla_reporte.html", params)
        else:
            output = BytesIO()

            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet()

            archivo_imagen = settings.MEDIA_ROOT+'\imagenes\promaco-logo.png'

            worksheet.insert_image('B2', archivo_imagen)
            worksheet.write(5, 1, "REPORTE DE PLANILLA")
            worksheet.write(6, 1, "Desde: " + vdesde)
            worksheet.write(7, 1, "Hasta: " + vhasta)

            rows = 9
            columns = 0
            for columna in params["columnas"]:                
                worksheet.write(rows, columns, columna["title"])
                columns += 1

            for registro in params["empleados"]:
                columns = 0
                rows += 1
                worksheet.write(rows, columns, registro["codigo"])
                columns += 1
                worksheet.write(rows, columns, registro["nombre"])
                columns += 1
                worksheet.write(rows, columns, registro["departamento"])
                for ingreso in registro["ingresos"]:
                    columns += 1
                    valor = ingreso["valor"].replace(',', '')
                    worksheet.write_number(rows, columns, float(valor))
                columns += 1
                valor = registro["total_ingresos"].replace(',', '')
                worksheet.write_number(rows, columns, float(valor))
                for deduccion in registro["deducciones"]:
                    columns += 1
                    valor = deduccion["valor"].replace(',', '')
                    worksheet.write_number(rows, columns, float(valor))
                columns += 1
                valor = registro["total_deducciones"].replace(',', '')
                worksheet.write_number(rows, columns, float(valor))
                columns += 1
                valor = registro["total_neto"].replace(',', '')
                worksheet.write_number(rows, columns, float(valor))

            columns = 2                
            filas_v = rows + 2
            worksheet.merge_range('A'+ str(filas_v) + ":" + "C" + str(filas_v), "Total")
            rows += 1
            for foot in params["footer"]:
                columns += 1
                valor = foot["valor"].replace(',', '')
                worksheet.write(rows, columns, float(valor))

            
            workbook.close()
            output.seek(0)

            nombre_archivo = "Planilla " + fecha_desde+"_" + fecha_hasta + ".xlsx"

            filename = nombre_archivo
            response = HttpResponse(
                output,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename

            return response

class ReporteBoletas(View):
    def get(self, request):
        totales = []
        l_detalle = []
        q_list = []
        planilla_id = request.GET.get("cboPlanilla")
        departamento_id = request.GET.get("cboDepartamento")
        if int(planilla_id) > 0:
            q_list.append(Q(planilla_id=planilla_id, active=True))
        if int(departamento_id) > 0:
            q_list.append(Q(empleado__dept__id=departamento_id))
        obj_planilla = Planilla.objects.get(pk=planilla_id)
        planilla_detalles = PlanillaDetalle.objects.filter(functools.reduce(operator.and_, q_list))
        #objects.filter(functools.reduce(operator.and_, q_list))
        # if departamento_id > 0:
        #     obj_depto = get_object_or_404(Department, pk=departamento_id)
        #     if obj_depto:
        #         planilla_detalles = PlanillaDetalle.objects.filter(planilla_id=planilla_id, empleado__dept=obj_depto, active=True)
        #     else:
        #         planilla_detalles = PlanillaDetalle.objects.filter(planilla_id=planilla_id, active=True)
        # else:
        #     planilla_detalles = PlanillaDetalle.objects.filter(planilla_id=planilla_id, active=True)
        ingresos = PlanillaDetalleIngresos.objects.filter(planilla=obj_planilla)
        deducciones = PlanillaDetalleDeducciones.objects.filter(planilla=obj_planilla)
        for e in planilla_detalles:
            suma_ingresos = 0
            suma_deducciones = 0
            l_ingreso = []
            l_deduccion = []
            for i in ingresos:
                if e.empleado.extEmpNo == i.empleado.extEmpNo:
                    detalle_i = {
                        'id': i.pk,
                        'ingreso': i.ingreso,
                        'valor': formato_millar(i.valor),
                    }
                    l_ingreso.append(detalle_i)
            for o in deducciones:
                if e.empleado.extEmpNo == o.empleado.extEmpNo:
                    detalle_d = {
                        'id': o.pk,
                        'deduccion': o.deduccion,
                        'valor': formato_millar(o.valor),
                    }
                    l_deduccion.append(detalle_d)
            obj_det = {
                'id': e.pk,
                'empleado': {'id': e.empleado.pk, 'primer_nombre': e.empleado.firstName, 'segundo_nombre': e.empleado.middleName, 'apellido': e.empleado.lastName, 'codigo': e.empleado.extEmpNo, 'cuenta': e.empleado.bankAccount},
                'planilla': {'id': e.planilla.pk, 'fecha_pago': e.planilla.fecha_pago, 'fecha_inicio': e.planilla.fecha_inicio, 'fecha_fin': e.planilla.fecha_fin},
                'dias_trabajados': int(e.dias_salario) - int(e.dias_ausentes_sin_pago),
                'ingresos': l_ingreso,
                'deducciones': l_deduccion,
                'suma_ingresos': formato_millar(e.total_ingresos),
                'suma_deducciones': formato_millar(e.total_deducciones),
                'total_neto': formato_millar(e.total_ingresos - e.total_deducciones),
            }
            l_detalle.append(obj_det)
        params = {
            'planilla_detalles': l_detalle,
            'ingresos': ingresos,
            'deducciones': deducciones,
            'totales': totales,
        }
        return Render.render("reportes/boletas_pago.html", params)

class ReportePlanillaExcel(View):

    def get(self, request):
        #Crear en memoria un archivo para el nuevo workbook
        output = BytesIO()

        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        for row_num, columns in enumerate(data):
            for col_num, cell_data in enumerate(columns):
                worksheet.write(row_num, col_num, cell_data)

        workbook.close()
        output.seek(0)

        filename = 'django_simple.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response

# def show_excel(request):
#    wb = Workbook()
#    ws0 = wb.add_sheet('0')

#    for x in range(10):
#       for y in range(10):
#          # writing to a specific x,y
#          ws0.write(x,y,"this is cell %s, %s" % (x,y))

#       wb.save('output.xls')
#    return HttpResponse(open('output.xls','r').read(),
#       mimetype='application/ms-excel')

class ReportePersonasPDF(View):
    
    def cabecera(self, pdf):
        archivo_imagen = settings.MEDIA_ROOT+'\imagenes\promaco-logo.png'
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90, preserveAspectRatio=True)

    def tabla(self,pdf,y):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Tipo de Deducción')
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [(tipo_ded.deduccion_tipo) for tipo_ded in DeduccionTipo.objects.all()]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[2 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(0,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black), 
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla 
        detalle_orden.wrapOn(pdf, 800, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 60,y)

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        self.cabecera(pdf)
        y = 600
        self.tabla(pdf, y)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
