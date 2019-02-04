# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core import serializers
from django.core.serializers import serialize
from django.db.models import Count, Min, Sum, Avg
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from worksheet.forms import *
from worksheet.models import *
import datetime
from datetime import date
import json
import locale
locale.setlocale(locale.LC_ALL, '')

# Create your views here.
def verificaSucursal(request):
    if not "sucursal" in request.session:
        return HttpResponseRedirect("/salir/")
    else:
        if request.session["sucursal"] < 1:
            return HttpResponseRedirect("/salir/")

@login_required(login_url='/form/iniciar-sesion/')
def home(request):
    verificaSucursal(request)
    empleados = Employee.objects.all()
    print request.session["sucursal"]
    return render(request, 'index.html', {'empleados':empleados})

def inicia_sesion(request):
    return render(request, 'iniciar-sesion.html')

# def login(request):
#     print "Entra aqui"
#     logout(request)
#     username = password = ''
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             login(user)
#             return HttpResponseRedirect('/')
#     return render(request, 'index.html')

def ingresar(request):
    Sucursales = None

    if not request.user.is_anonymous():
        return HttpResponseRedirect('/form/iniciar-sesion/')
    
    
    if request.method == 'POST':
        frmSesion = AuthenticationForm(request.POST)
        usuario = request.POST['username']
        clave = request.POST['password']
        acceso = authenticate(username=usuario, password=clave)
        
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                totReg = UsuarioSucursal.objects.filter(usuario=request.user, active = True).count()    
                if totReg > 0:
                    if totReg > 1:
                        return HttpResponseRedirect('/seleccionar/sucursal/')
                    else:
                        sucursal = UsuarioSucursal.objects.get(usuario=request.user, active=True)
                        request.session["nombre_sucursal"] = sucursal.sucursal.name
                        request.session["sucursal"] = sucursal.sucursal.pk
                        return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/salir/')
            else:
                return render(request, 'no-activo.html')
        else:
            return render(request, 'no-usuario.html')
    else:
        frmSesion = AuthenticationForm()
        return HttpResponseRedirect('/form/iniciar-sesion/')


@login_required(login_url='/form/iniciar-sesion/')
def seleccionar_sucursal(request):
    empresas= []
    empresa = {}
    sucursales = UsuarioSucursal.objects.filter(usuario=request.user)
    empresa_flat = UsuarioSucursal.objects.filter(usuario=request.user).values_list('sucursal__empresa_id', flat=True).distinct()
    empresas = Empresa.objects.filter(pk__in=empresa_flat)
    return render(request, 'seleccionar_sucursal.html', {'sucursales':sucursales, 'empresas':empresas})

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

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.add_employee', raise_exception=True)
def empleado_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    verificaSucursal(request)
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
    civil_status = CivilStatus.objects.filter(active=True)
    salary_units = SalaryUnit.objects.filter(active=True, empresa_reg=suc.empresa)
    costs_units = CostUnit.objects.filter(active=True, empresa_reg=suc.empresa)
    banks = Bank.objects.filter(active=True)
    tipos_contratos = TipoContrato.objects.filter(active=True, empresa_reg=suc.empresa)
    tipos_nominas = TipoNomina.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, 'empleado-form.html', {'banks':banks, 'costs_units': costs_units, 'salary_units': salary_units, 'civil_status':civil_status, 'citizenships':citizenships, 'positions':positions, 'departments':departments, 'branches':branches, 'salesPersons':salesPersons, 'states':states, 'countries':countries, 'stats':estados_emp, 'terms':terms, 'sexs':sexos, 'empleados':empleados, 'tipos_contratos':tipos_contratos, 'tipos_nominas':tipos_nominas})

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.change_employee', raise_exception=True)
def empleado_editar(request, id):
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
    return render(request, 'empleado-form.html', {'editar':True, 'dato':dato, 'banks':banks, 'costs_units': costs_units, 'salary_units': salary_units, 'civil_status':civil_status, 'citizenships':citizenships, 'positions':positions, 'departments':departments, 'branches':branches, 'salesPersons':salesPersons, 'states':states, 'countries':countries, 'stats':estados_emp, 'terms':terms, 'sexs':sexos, 'empleados':empleados, 'tipos_contratos':tipos_contratos, 'tipos_nominas':tipos_nominas})
    #return render(request, 'empleado-form.html', {'editar':True, 'dato':dato, 'positions':positions, 'departments':departments, 'branches':branches, 'salesPersons':salesPersons})

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.see_employee', raise_exception=True)
def empleado_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'empleado-listado.html', {'empleados':empleados})

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.see_reg_employee', raise_exception=True)
def empleado_perfil(request, id):
    dato = Employee.objects.get(pk=id)
    tot_reg = ImagenEmpleado.objects.filter(empleado__id=id).count()
    if tot_reg > 0:
        imagen = ImagenEmpleado.objects.get(empleado__id=id)
    else:
        imagen = None
    return render(request, 'perfil-empleado.html', {'dato':dato, 'imagen': imagen})

@login_required(login_url='/form/iniciar-sesion/')
def corporativo(request):
    return render(request, 'corporativo.html')

@login_required(login_url='/form/iniciar-sesion/')
def corporativo_editar(request, reg_id):
    dato = GrupoCorporativo.objects.get(pk=reg_id)
    return render(request, 'corporativo.html', {'dato':dato, 'editar':True})

@login_required(login_url='/form/iniciar-sesion/')
def listadoCorporativo(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    corporativos = GrupoCorporativo.objects.filter(empresa_reg=suc.empresa).order_by('date_reg')
    return render(request, 'corporativo-listado.html', {'corporativos':corporativos})

@login_required(login_url='/form/iniciar-sesion/')
def empresa(request):
    return render(request, 'empresa.html')

@login_required(login_url='/form/iniciar-sesion/')
def empresa_editar(request, emp_id):
    dato = Empresa.objects.get(pk=emp_id)
    return render(request, 'empresa.html', {'dato':dato, 'editar':True} )

@login_required(login_url='/form/iniciar-sesion/')
def listadoEmpresa(request):
    empresas = Empresa.objects.all()
    return render(request, 'empresa-listado.html', {'empresas':empresas})

@login_required(login_url='/form/iniciar-sesion/')
def sucursal(request):
    return render(request, 'sucursal.html')

@login_required(login_url='/form/iniciar-sesion/')
def sucursal_editar(request, id):
    dato = Branch.objects.get(pk=id)
    return render(request, 'sucursal.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def listadoSucursal(request):
    sucursales = Branch.objects.all()
    return render(request, 'sucursal-listado.html', {'sucursales':sucursales})

@login_required(login_url='/form/iniciar-sesion/')
def divisiones(request):
    return render(request, 'divisiones.html')

@login_required(login_url='/form/iniciar-sesion/')
def division_editar(request, id):
    dato = Divisiones.objects.get(pk=id)
    return render(request, 'divisiones.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def listadoDivisiones(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    divisiones = Divisiones.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'divisiones-listado.html', {'divisiones':divisiones})

@login_required(login_url='/form/iniciar-sesion/')
def departamentos(request):
    return render(request, 'departamentos.html')

@login_required(login_url='/form/iniciar-sesion/')
def departamento_editar(request, id):
    dato = Department.objects.get(pk=id)
    return render(request, 'departamentos.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def listadoDepartamentos(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    deptos = Department.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(request, 'departamento-listado.html', {'deptos':deptos})

@login_required(login_url='/form/iniciar-sesion/')
def puestoTrabajo(request):
    return render(request, 'puesto-trabajo.html')

@login_required(login_url='/form/iniciar-sesion/')
def puesto_editar(request, id):
    dato = Position.objects.get(pk=id)
    return render(request, 'puesto-trabajo.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def listadoPuestoTrabajo(request):
    verificaSucursal(request)
    suc = Branch.objects.get(pk=request.session["sucursal"])
    print suc.empresa_id
    puestos = Position.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, 'puestos-listado.html', {'puesto':puestos})

@login_required(login_url='/form/iniciar-sesion/')
def centro_costos(request):
    return render(request, 'centro-costos.html')

@login_required(login_url='/form/iniciar-sesion/')
def centro_costo_editar(request, id):
    dato = CentrosCostos.objects.get(pk=id)
    return render(request, 'centro-costos.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def listadoCentroCostos(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    ccostos = CentrosCostos.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'ccostos-listado.html', {'ccostos':ccostos})

@login_required(login_url='/form/iniciar-sesion/')
def paises(request):
    return render(request, 'paises.html')

@login_required(login_url='/form/iniciar-sesion/')
def paises_editar(request, id):
    dato = Country.objects.get(pk=id)
    return render(request, 'paises.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def listadoPaises(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    paises = Country.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'paises-listado.html', {'paises':paises})

@login_required(login_url='/form/iniciar-sesion/')
def deptos_pais(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    paises = Country.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'deptos-pais.html', {'paises':paises})

@login_required(login_url='/form/iniciar-sesion/')
def deptos_pais_editar(request, id):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    dato = State.objects.get(pk=id)
    paises = Country.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'deptos-pais.html', {'editar':True, 'dato':dato, 'paises':paises})

@login_required(login_url='/form/iniciar-sesion/')
def deptos_pais_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    deptos = State.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'deptos-pais-listado.html', {'deptos': deptos})

@login_required(login_url='/form/iniciar-sesion/')
def ciudad(request):
    return render(request, 'ciudad.html')

@login_required(login_url='/form/iniciar-sesion/')
def ciudad_editar(request, id):
    dato = Ciudad.objects.get(pk=id)
    return render(request, 'ciudad.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def ciudades_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    ciudades = Ciudad.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'ciudades-listado.html', {'ciudades':ciudades})

@login_required(login_url='/form/iniciar-sesion/')
def genero(request):
    return render(request, 'genero.html')

@login_required(login_url='/form/iniciar-sesion/')
def genero_editar(request, id):
    dato = Sex.objects.get(pk=id)
    return render(request, 'genero.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def generos_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    generos = Sex.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'genero-listado.html', {'generos':generos})

@login_required(login_url='/form/iniciar-sesion/')
def estado_civil(request):
    return render(request, 'estado-civil.html')

@login_required(login_url='/form/iniciar-sesion/')
def estado_civil_editar(request, id):
    dato = CivilStatus.objects.get(pk=id)
    return render(request, 'estado-civil.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def estado_civil_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    estados = CivilStatus.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'estado-civil-listado.html', {'estados':estados})

@login_required(login_url='/form/iniciar-sesion/')
def parentesco(request):
    return render(request, 'parentesco.html')

@login_required(login_url='/form/iniciar-sesion/')
def parentesco_editar(request, id):
    dato = Parentesco.objects.get(pk=id)
    return render(request, 'parentesco.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def parentesco_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    parentescos = Parentesco.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'parentesco-listado.html', {'parentescos':parentescos})

@login_required(login_url='/form/iniciar-sesion/')
def funcion_trabajo(request):
    return render(request, 'funciones-trabajo.html')

@login_required(login_url='/form/iniciar-sesion/')
def funcion_trabajo_editar(request, id):
    funcion = FuncionesTrabajo.objects.get(pk=id)
    return render(request, 'funciones-trabajo.html', {'dato':funcion, 'editar':True})

@login_required(login_url='/form/iniciar-sesion/')
def funcion_trab_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    funciones = FuncionesTrabajo.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'funciones-trabajo-listado.html', {'funciones': funciones})

@login_required(login_url='/form/iniciar-sesion/')
def equipo_trabajo(request):
    return render(request, 'equipo-trabajo.html' )

@login_required(login_url='/form/iniciar-sesion/')
def equipo_trabajo_editar(request, id):
    dato = EquipoTrabajo.objects.get(pk=id)
    return render(request, 'equipo-trabajo.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def equipo_trabajo_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    equipos = EquipoTrabajo.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'equipo-trabajo-listado.html', {'equipos':equipos})

@login_required(login_url='/form/iniciar-sesion/')
def estado_empleado(request):
    return render(request, 'estatus-empleado.html')

@login_required(login_url='/form/iniciar-sesion/')
def estado_empleado_editar(request, id):
    dato = StatusEmp.objects.get(pk=id)
    return render(request, 'estatus-empleado.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def estado_empleado_listado(request):
    lista = StatusEmp.objects.all()
    return render(request, 'estado-empleado-listado.html', {'lista':lista})

@login_required(login_url='/form/iniciar-sesion/')
def ausentismo(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    motivos = MotivosAusencia.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, 'ausentismo.html', {'empleados':empleados, 'motivos':motivos})

@login_required(login_url='/form/iniciar-sesion/')
def ausentismo_editar(request, id):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    dato = Ausentismo.objects.get(pk=id)
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, 'ausentismo.html', {'editar':True, 'dato':dato, 'empleados':empleados})

@login_required(login_url='/form/iniciar-sesion/')
def ausentismo_listado(request):
    lista = []
    busqueda = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.all()
    if 'empleado' in request.GET:
        emp = request.GET.get("empleado")
        if len(emp) > 0:
            if int(emp) > 0:
                busqueda = int(emp)
                empleado = Employee.objects.get(pk=busqueda)
                print empleado
                lista = Ausentismo.objects.filter(empleado=empleado, empresa_reg = suc.empresa)
            else:
                lista = Ausentismo.objects.filter(sucursal_reg=suc)[:50]
        else:
            lista = Ausentismo.objects.filter(sucursal_reg=suc)[:50]
    else:
        lista = Ausentismo.objects.filter(sucursal_reg=suc)[:50]
    #lista = Ausentismo.objects.all().order_by('-desde')
    #empleados = Employee.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'ausentismo-listado.html', {'datos':lista, 'empleados': empleados, 'busqueda':busqueda})

@login_required(login_url='/form/iniciar-sesion/')
def motivos_ausencia(request):
    return render(request, 'motivos-ausencia.html')

@login_required(login_url='/form/iniciar-sesion/')
def motivos_ausencia_editar(request, id):
    dato = MotivosAusencia.objects.get(pk=id)
    return render(request, 'motivos-ausencia.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def motivos_ausencia_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista = MotivosAusencia.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'motivos-ausencia-listado.html', {'lista':lista})

@login_required(login_url='/form/iniciar-sesion/')
def motivo_despido(request):
    return render(request, 'motivos-despido.html')

@login_required(login_url='/form/iniciar-sesion/')
def motivo_despido_editar(request, id):
    dato = MotivosDespido.objects.get(pk=id)
    return render(request, 'motivos-despido.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def motivos_despido_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista = MotivosDespido.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'motivos-despido-listado.html', {'lista':lista})

@login_required(login_url='/form/iniciar-sesion/')
def motivos_renuncia(request):
    return render(request, 'motivos-renuncia.html')

@login_required(login_url='/form/iniciar-sesion/')
def motivos_renuncia_editar(request, id):
    dato = MotivosRenuncia.objects.get(pk=id)
    return render(request, 'motivos-renuncia.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def motivos_renuncia_listado(request):
    lista = MotivosRenuncia.objects.all()
    return render(request, 'motivos-renuncia-listado.html', {'lista':lista})

@login_required(login_url='/form/iniciar-sesion/')
def clase_educacion(request):
    return render(request, 'clase-educacion.html')

@login_required(login_url='/form/iniciar-sesion/')
def clase_educacion_editar(request, id):
    dato = ClaseEducacion.objects.get(pk=id)
    return render(request, 'clase-educacion.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def clase_educacion_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista = ClaseEducacion.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'clase-educacion-listado.html',{'lista':lista})

@login_required(login_url='/form/iniciar-sesion/')
def motivos_aumento_sueldo(request):
    return render(request, 'motivos-aumento-sueldo.html')

@login_required(login_url='/form/iniciar-sesion/')
def motivos_aumento_sueldo_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista = MotivoAumentoSueldo.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'motivos-aumento-sueldo-listado.html', {'lista': lista})

@login_required(login_url='/form/iniciar-sesion/')
def motivo_aumento_sueldo_editar(request, id):
    dato = MotivoAumentoSueldo.objects.get(pk=id)
    return render(request, 'motivos-aumento-sueldo.html', {'editar': True, 'dato': dato})

@login_required(login_url='/form/iniciar-sesion/')
def educacion(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    clases_educacion = ClaseEducacion.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, 'educacion.html', {'empleados': empleados, 'clasesEducacion':clases_educacion})

@login_required(login_url='/form/iniciar-sesion/')
def educacion_editar(request, id):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    clases_educacion = ClaseEducacion.objects.filter(active=True, empresa_reg=suc.empresa)
    dato = Educacion.objects.get(pk=id)
    return render(request, 'educacion.html', {'editar':True, 'dato':dato, 'empleados':empleados, 'clasesEducacion':clases_educacion})

@login_required(login_url='/form/iniciar-sesion/')
def educacion_listar(request):
    datos = []
    busqueda = None

    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(empresa_reg=suc.empresa)
    if 'empleado' in request.GET:
        emp = request.GET.get("empleado")
        if len(emp) > 0:
            if int(emp) > 0:
                busqueda = int(emp)
                datos = Educacion.objects.filter(empleado__pk=emp, empresa_reg=suc.empresa)
    return render(request, 'educacion-listado.html', {'datos':datos, 'empleados':empleados, 'busqueda':busqueda})

@login_required(login_url='/form/iniciar-sesion/')
def evaluacion(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, 'evaluacion.html', {'empleados':empleados})

@login_required(login_url='/form/iniciar-sesion/')
def evaluacion_listar(request):
    datos = []
    busqueda = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.all()
    if 'empleado' in request.GET:
        emp = request.GET.get("empleado")
        if len(emp) > 0:
            if int(emp) > 0:
                busqueda = int(emp)
                datos = Evaluacion.objects.filter(empleado__pk=emp, empresa_reg=suc.empresa)
    return render(request, 'evaluaciones-listado.html', {'datos':datos, 'empleados':empleados, 'busqueda': busqueda})

@login_required(login_url='/form/iniciar-sesion/')
def evaluacion_editar(request, id):
    empleados = Employee.objects.filter(active=True)
    dato = Evaluacion.objects.get(pk=id)
    return render(request, 'evaluacion.html', {'editar': True, 'dato': dato, 'empleados': empleados})

@login_required(login_url='/form/iniciar-sesion/')
def empleo_anterior_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, 'empleos-anteriores.html', {'empleados':empleados})

@login_required(login_url='/form/iniciar-sesion/')
def empleo_anterior_editar(request, id):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    dato = EmpleosAnteriores.objects.get(pk=id)
    return render(request, 'empleos-anteriores.html', {'editar': True, 'dato': dato, 'empleados': empleados})

@login_required(login_url='/form/iniciar-sesion/')
def empleo_anterior_listar(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    datos = []
    busqueda = None
    empleados = Employee.objects.filter(empresa_reg=suc.empresa)
    if 'empleado' in request.GET:
        emp = request.GET.get("empleado")
        if len(emp) > 0:
            if int(emp) > 0:
                busqueda = int(emp)
                datos = EmpleosAnteriores.objects.filter(empleado__pk=emp)
    return render(request, 'empleos-anteriores-listado.html', {'datos':datos, 'empleados':empleados, 'busqueda':busqueda})

@login_required(login_url='/form/iniciar-sesion/')
def grupo_comision(request):
    return render(request, 'grupo-comisiones.html')

@login_required(login_url='/form/iniciar-sesion/')
def grupo_comision_ditar(request, id):
    dato = GrupoComisiones.objects.get(pk=id)
    return render(request, 'grupo-comisiones.html', {'editar': True, 'dato': dato})

@login_required(login_url='/form/iniciar-sesion/')
def grupo_comisiones_listar(request):
    datos = GrupoComisiones.objects.all()
    return render(request, 'grupo-comisiones-listado.html', {'datos':datos})

@login_required(login_url='/form/iniciar-sesion/')
def vendedor_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    grp_com = GrupoComisiones.objects.filter(empresa_reg=suc.empresa)
    empl_list = Vendedor.objects.filter(empresa_reg=suc.empresa).values_list('empleado__id', flat=True)
    empleados = Employee.objects.exclude(pk__in=empl_list)
    print empl_list
    #empleados = Employee.objects.filter(active=True)
    return render(request, 'vendedor.html', {'grp_com':grp_com, 'empleados':empleados, 'editar':False})

@login_required(login_url='/form/iniciar-sesion/')
def vendedor_editar(request, id):
    empleados = Employee.objects.filter(active=True)
    grp_com = GrupoComisiones.objects.all()
    dato = Vendedor.objects.get(pk=id)
    return render(request, 'vendedor.html', {'editar': True, 'dato': dato, 'empleados': empleados, 'grp_com': grp_com})

@login_required(login_url='/form/iniciar-sesion/')
def vendedor_listar(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    datos = Vendedor.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'vendedor-listado.html', {'datos':datos})

@login_required(login_url='/form/iniciar-sesion/')
def feriado_form(request):
    return render(request, 'feriado.html')

@login_required(login_url='/form/iniciar-sesion/')
def feriado_editar(request, id):
    dato = Feriado.objects.get(pk=id)
    return render(request, 'feriado.html', {'editar': True, 'dato': dato})

@login_required(login_url='/form/iniciar-sesion/')
def feriado_listar(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    datos = Feriado.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'feriado-listado.html', {'datos':datos})

@login_required(login_url='/form/iniciar-sesion/')
def articulo_asignado_form(request):
    return render(request, 'activo-asignado.html')

@login_required(login_url='/form/iniciar-sesion/')
def articulo_asignado_editar(request, id):
    dato = ActivoAsignado.objects.get(pk=id)
    return render(request, 'activo-asignado.html', {'editar': True, 'dato': dato})

@login_required(login_url='/form/iniciar-sesion/')
def articulos_asignados_listar(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    datos = ActivoAsignado.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'activos-asignados-listado.html', {'datos':datos})

@login_required(login_url='/form/iniciar-sesion/')
def motivo_rescision_contrato_form(request):
    return render(request, 'motivos-rescision-contrato-form.html')

@login_required(login_url='/form/iniciar-sesion/')
def motivo_rescision_contrato_editar(request, id):
    dato = TermReason.objects.get(pk=id)
    return render(request, 'motivos-rescision-contrato-form.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def motivo_rescicion_contrato_listar(request):
    lista = TermReason.objects.all()
    return render(request, 'motivo-rescision-contrato-listado.html', {'lista':lista})

@login_required(login_url='/form/iniciar-sesion/')
def tipo_salario_form(request):
    return render(request, 'tipo-salario-form.html')

@login_required(login_url='/form/iniciar-sesion/')
def tipo_salario_editar(request, id):
    dato = SalaryUnit.objects.get(pk=id)
    return render(request, 'tipo-salario-form.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
def tipo_salario_listar(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista = SalaryUnit.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'tipo-salario-listado.html', {'lista':lista})

@login_required(login_url='/form/iniciar-sesion/')
def tipo_costo_empleado_form(request):
    return render(request, 'costo-empleado-form.html')

@login_required(login_url='/form/iniciar-sesion/')
def tipo_costo_empleado_editar(request, id):
    dato = CostUnit.objects.get(pk=id)
    return render(request, 'costo-empleado-form.html', {'editar': True, 'dato': dato})

@login_required(login_url='/form/iniciar-sesion/')
def tipo_costo_empleado_listar(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista = CostUnit.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'costo-empleado-listado.html', {'lista':lista})

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.add_banco', raise_exception=True)
def banco_form(request):
    return render(request, 'banco-form.html')

@login_required(login_url='/form/iniciar-sesion/')
def banco_editar(request, id):
    dato = Bank.objects.get(pk=id)
    return render(request, 'banco-form.html', {'editar':True, 'dato':dato})

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.see_banco', raise_exception=True)
def banco_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista = Bank.objects.filter(empresa_reg=suc.empresa)
    return render(request, 'banco-listado.html', {'lista':lista})

@login_required(login_url='/form/iniciar-sesion/')
def usuario_empresa_form(request):
    frm = UsuarioEmpresaForm()
    users = User.objects.all()
    empresas = Empresa.objects.all()
    return render(request, 'usuario-empresa.html', {'frm':frm, 'users':users, 'empresas':empresas})

@login_required(login_url='/form/iniciar-sesion/')
def usuario_empresa_listar(request):
    lista = UsuarioEmpresa.objects.all()
    return render(request, 'usuario-empresa-listado.html', {'lista': lista})

@login_required(login_url='/form/iniciar-sesion/')
def usuario_empresa_editar(request, id):
    dato = UsuarioEmpresa.objects.get(pk=id)
    users = User.objects.all()
    empresas = Empresa.objects.all()
    return render(request, 'usuario-empresa.html', {'editar':True, 'dato':dato, 'users':users, 'empresas':empresas})


#---------------------------->>>> VISTAS AJAX <<<<----------------------------#
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
        if  request.is_ajax():
            if request.method == 'POST':
                pNom = request.POST['pNom']
                sNom = request.POST['sNom']
                apellido = request.POST['apellido']
                puesto = request.POST['puesto']
                no_ext = request.POST['numExt']
                activo = request.POST['activo']
                pos = request.POST['pos']
                telOf = request.POST['telOf']
                dept = request.POST['dept']
                telExt = request.POST['telExt']
                suc = request.POST['suc']
                jefe = request.POST['jefe']
                telMov = request.POST['telMov']
                pag = request.POST['pag']
                slsP = request.POST['slsP']
                fax = request.POST['fax']
                email = request.POST['email']
                telCasa = request.POST['telCasa']
                calle = request.POST['calle']
                ncalle = request.POST['nCalle']
                bloque = request.POST['bloque']
                edif = request.POST['edif']
                codPos = request.POST['codPos']
                ciudad = request.POST['ciudad']
                condado = request.POST['condado']
                hdept = request.POST['hdept']
                hpais = request.POST['hpais']
                wcalle = request.POST['wcalle']
                wncalle = request.POST['wncalle']
                wbloque = request.POST['wbloque']
                wedif = request.POST['wedif']
                wcodPos = request.POST['wcodPost']
                wciudad = request.POST['wciudad']
                wcondado = request.POST['wcondado']
                wdept = request.POST['wdept']
                wpais = request.POST['wpais']
                fechaCont = request.POST['fechaCont']
                estEmp = request.POST['estEmp']
                fechaRes = request.POST['fechaRES']
                term = request.POST['term']
                sexo = request.POST['sexo']
                fecNac = request.POST['fecNac']
                lugNac = request.POST['lugNac']
                estCivil = request.POST['estCivil']
                cantHijos = request.POST['cantHijos']
                govID = request.POST['numID']
                citiz = request.POST['citiz']
                numPass = request.POST['numPass']
                fecPassExt = request.POST['fecPassExt']
                fecEmis = request.POST['fecEmis']
                emisor = request.POST['emisor']
                salary = request.POST['salario']
                salario_diario = request.POST['salario_diario']
                salaryUnits = request.POST['salarioUnd']
                empCost = request.POST['costEmp']
                empCostUnit = request.POST['costEmpUni']
                banco = request.POST['banco']
                numCuenta = request.POST['numCuenta']
                branchBank = request.POST['bankSucursal']
                remark = request.POST['comentarios']

                if len(pNom) == 0:
                    mensaje = "El campo 'Primer Nombre' es obligatorio."
                    data = {
                        'mensaje':mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(sNom) > 0:
                    vSegundoNombre = sNom

                if len(apellido) == 0:
                    mensaje = "El campo 'Apellido' es obligatorio."
                    data = {
                        'mensaje':mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(puesto) == 0:
                    mensaje = "El campo 'Puesto de trabajo' es obligatorio."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(no_ext) == 0:
                    no_ext = None

                if len(pos) > 0:
                    if int(pos) > 0:
                        oPosicion = Position.objects.get(pk=pos)
                        if not oPosicion:
                            mensaje = "El 'Puesto de trabajo' no existe."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(dept) > 0:

                    if int(dept) > 0:
                        oDepartamento = Department.objects.get(pk=dept)
                        if not oDepartamento:
                            mensaje = "El 'Departamento' no existe."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(suc) > 0:
                    if int(suc) > 0:
                        oSucursal = Branch.objects.get(pk=suc)
                        if not oSucursal:
                            mensaje = "El 'Sucursal' no existe."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(jefe) > 0:
                    if int(jefe) > 0:
                        oJefe = Employee.objects.get(pk=jefe)
                        if not oJefe:
                            mensaje = "El 'Gerente' no existe."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(slsP) > 0:
                    if int(slsP) > 0:
                        oEmpVentas = Vendedor.objects.get(pk=slsP)
                        if not oSucursal:
                            mensaje = "El 'empleado de ventas' no existe."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(telOf) == 0:
                    telOf = None

                
                if len(telExt) == 0:
                    telExt = None

                if len(telMov) == 0:
                    telMov = None

                if len(pag) == 0:
                    pag = None

                if len(telCasa) == 0:
                    telCasa == None

                if len(fax) == 0:
                    fax = None

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
                
                

                if len(hdept) > 0:
                    if int(hdept) > 0:
                        oEstado = State.objects.get(pk=hdept)
                        if not oEstado:
                            mensaje = "El 'Estado/Departamento' no existe."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(hpais) > 0:
                    if int(hpais) > 0:
                        oPais = Country.objects.get(pk=hpais)
                        if not oPais:
                            mensaje = "El pais no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
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

                if len(wdept) > 0:
                    if int(wdept) > 0:
                        oEstadoTrabajo = State.objects.get(pk=wdept)
                        if not oEstadoTrabajo:
                            mensaje = "El estado de trabajo no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(wpais) > 0:
                    if int(wpais) > 0:
                        oPaisTrabajo = Country.objects.get(pk=wpais)
                        if not oPaisTrabajo:
                            mensaje = "El país de trabajo no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(fechaCont) == 0:
                    fechaCont = None

                if len(estEmp) > 0:
                    if int(estEmp) > 0:
                        oEstadoEmpleado = StatusEmp.objects.get(pk=estEmp)
                        if not oEstadoEmpleado:
                            mensaje = "El estado de empleado no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(fechaRes) == 0:
                    fechaRes = None

                if len(term) > 0:
                    if int(term) > 0:
                        oTerminoRescision = TermReason.objects.get(pk=term)
                        if not oTerminoRescision:
                            mensaje = "El término de rescisión no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(sexo) > 0:
                    if int(sexo) > 0:
                        oSex = Sex.objects.get(pk=sexo)
                        if not oSex:
                            mensaje = "El sexo no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(fecNac) == 0:
                    fecNac = None

                if len(lugNac) > 0:
                    if int(lugNac) > 0:
                        oBirthCountry = Country.objects.get(pk=lugNac)
                        if not oBirthCountry:
                            mensaje = "El lugar de nacimiento no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(estCivil) > 0:
                    if int(estCivil) > 0:
                        oCivilStatus = CivilStatus.objects.get(pk=estCivil)
                        if not oCivilStatus:
                            mensaje = "El estado civil no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(citiz) > 0:
                    if int(citiz) > 0:
                        oCitizenShip = Country.objects.get(pk=citiz)
                        if not oCitizenShip:
                            mensaje = "La nacionalidad no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
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
                            mensaje = "El tipo de salario no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(empCostUnit) > 0:
                    if int(empCostUnit) > 0:
                        oEmpCostUnit = CostUnit.objects.get(pk=empCostUnit)
                        if not oEmpCostUnit:
                            mensaje = "El tipo de costo de empleado no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(banco) > 0:
                    if int(banco) > 0:
                        print "LLego aqui"
                        oBankCode = Bank.objects.get(pk=banco)
                        
                        if not oBankCode:
                            mensaje = "El banco no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
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
                    middleName = vSegundoNombre,
                    lastName=apellido,
                    extEmpNo=no_ext,
                    jobTitle=puesto,
                    user_reg=request.user,
                    active = activo,
                    position = oPosicion,
                    officeTel = telOf,
                    dept = oDepartamento,
                    officeExt = telExt,
                    branch = oSucursal,
                    jefe = oJefe,
                    mobile=telMov,
                    pager = pag,
                    slsPerson = oEmpVentas,
                    fax = fax,
                    email = email,
                    homeTel = telCasa,
                    homeStreet = calle,
                    streetNoH = ncalle,
                    homeBlock = bloque,
                    homeBuild = edif,
                    homeZip = codPos,
                    homeCity = ciudad,
                    homeCounty = condado,
                    homeState = oEstado,
                    homeCountry = oPais,
                    workStreet = wcalle,
                    streetNoW = wncalle,
                    workBlock = wbloque,
                    workBuild = wedif,
                    workZip = wcodPos,
                    workCity = wciudad,
                    workCounty = wcondado,
                    workState = oEstadoTrabajo,
                    workCountry = oPaisTrabajo,
                    startDate = fechaCont,
                    status = oEstadoEmpleado,
                    termDate = fechaRes,
                    termReason = oTerminoRescision,
                    sex = oSex,
                    birthDate = fecNac,
                    birthCountry = oBirthCountry,
                    marrStatus = oCivilStatus,
                    nChildren = cantHijos,
                    govID = govID,
                    citizenship = oCitizenShip,
                    passportNo = numPass,
                    passportExt = fecPassExt,
                    passIssue = fecEmis,
                    passIssuer = emisor,
                    salary = salary,
                    salario_diario = salario_diario,
                    salaryUnits = oSalaryUnits,
                    empCost = empCost,
                    empCostUnit = oEmpCostUnit,
                    bankCode = oBankCode,
                    bankAccount = numCuenta,
                    branchBank = branchBank,
                    remark = remark,
                    empresa_reg = suc.empresa
                )
                oEmpleado.save()
                
                mensaje = 'Se ha guardado el registro del empleado'
                data = {
                    'mensaje':mensaje, 'error': False
                }
                return JsonResponse(data)
    except Exception as ex:
        data = {
            'error':True,
            'mensaje': 'Error: ' + ex.message,
        }
        print ex
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
        if  request.is_ajax():
            if request.method == 'POST':
                id = request.POST['id']
                pNom = request.POST['pNom']
                sNom = request.POST['sNom']
                apellido = request.POST['apellido']
                puesto = request.POST['puesto']
                no_ext = request.POST['numExt']
                activo = request.POST['activo']
                pos = request.POST['pos']
                telOf = request.POST['telOf']
                dept = request.POST['dept']
                telExt = request.POST['telExt']
                suc = request.POST['suc']
                jefe = request.POST['jefe']
                telMov = request.POST['telMov']
                pag = request.POST['pag']
                slsP = request.POST['slsP']
                fax = request.POST['fax']
                email = request.POST['email']
                telCasa = request.POST['telCasa']
                calle = request.POST['calle']
                ncalle = request.POST['nCalle']
                bloque = request.POST['bloque']
                edif = request.POST['edif']
                codPos = request.POST['codPos']
                ciudad = request.POST['ciudad']
                condado = request.POST['condado']
                hdept = request.POST['hdept']
                hpais = request.POST['hpais']
                wcalle = request.POST['wcalle']
                wncalle = request.POST['wncalle']
                wbloque = request.POST['wbloque']
                wedif = request.POST['wedif']
                wcodPos = request.POST['wcodPost']
                wciudad = request.POST['wciudad']
                wcondado = request.POST['wcondado']
                wdept = request.POST['wdept']
                wpais = request.POST['wpais']
                fechaCont = request.POST['fechaCont']
                estEmp = request.POST['estEmp']
                fechaRes = request.POST['fechaRES']
                term = request.POST['term']
                sexo = request.POST['sexo']
                fecNac = request.POST['fecNac']
                lugNac = request.POST['lugNac']
                estCivil = request.POST['estCivil']
                cantHijos = request.POST['cantHijos']
                govID = request.POST['numID']
                citiz = request.POST['citiz']
                numPass = request.POST['numPass']
                fecPassExt = request.POST['fecPassExt']
                fecEmis = request.POST['fecEmis']
                emisor = request.POST['emisor']
                salary = request.POST['salario']
                salario_diario = request.POST['salario_diario']
                salaryUnits = request.POST['salarioUnd']
                empCost = request.POST['costEmp']
                empCostUnit = request.POST['costEmpUni']
                banco = request.POST['banco']
                numCuenta = request.POST['numCuenta']
                branchBank = request.POST['bankSucursal']
                remark = request.POST['comentarios']
                tipo_nomina = request.POST['tipo_nomina']
                tipo_contrato = request.POST['tipo_contrato']

                if len(pNom) == 0:
                    mensaje = "El campo 'Primer Nombre' es obligatorio."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(sNom) == 0:
                    sNom = None

                if len(apellido) == 0:
                    mensaje = "El campo 'Apellido' es obligatorio."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(puesto) == 0:
                    mensaje = "El campo 'Puesto de trabajo' es obligatorio."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(no_ext) == 0:
                    no_ext = None

                if len(pos) > 0:
                    if int(pos) > 0:
                        oPosicion = Position.objects.get(pk=pos)
                        if not oPosicion:
                            mensaje = "El 'Puesto de trabajo' no existe."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(dept) > 0:
                    if int(dept) > 0:
                        oDepartamento = Department.objects.get(pk=dept)
                        if not oDepartamento:
                            mensaje = "El 'Departamento' no existe."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(suc) > 0:
                    if int(suc) > 0:
                        oSucursal = Branch.objects.get(pk=suc)
                        if not oSucursal:
                            mensaje = "El 'Sucursal' no existe."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(jefe) > 0:
                    if int(jefe) > 0:
                        oJefe = Employee.objects.get(pk=jefe)
                        if not oJefe:
                            mensaje = "El 'Gerente' no existe."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(slsP) > 0:
                    if int(slsP) > 0:
                        oEmpVentas = SalesPerson.objects.get(pk=slsP)
                        if not oSucursal:
                            mensaje = "El 'empleado de ventas' no existe."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(telOf) == 0:
                    telOf = None

                if len(telExt) == 0:
                    telExt = None

                if len(telMov) == 0:
                    telMov = None

                if len(pag) == 0:
                    pag = None

                if len(telCasa) == 0:
                    telCasa = None

                if len(fax) == 0:
                    fax = None

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

                if len(hdept) > 0:
                    if int(hdept) > 0:
                        oEstado = State.objects.get(pk=hdept)
                        if not oEstado:
                            mensaje = "El 'Estado/Departamento' no existe."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(hpais) > 0:
                    if int(hpais) > 0:
                        oPais = Country.objects.get(pk=hpais)
                        if not oPais:
                            mensaje = "El pais no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
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

                if len(wdept) > 0:
                    if int(wdept) > 0:
                        oEstadoTrabajo = State.objects.get(pk=wdept)
                        if not oEstadoTrabajo:
                            mensaje = "El estado de trabajo no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(wpais) > 0:
                    if int(wpais) > 0:
                        oPaisTrabajo = Country.objects.get(pk=wpais)
                        if not oPaisTrabajo:
                            mensaje = "El país de trabajo no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(fechaCont) == 0:
                    fechaCont = None

                if len(estEmp) > 0:
                    if int(estEmp) > 0:
                        oEstadoEmpleado = StatusEmp.objects.get(pk=estEmp)
                        if not oEstadoEmpleado:
                            mensaje = "El estado de empleado no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(fechaRes) == 0:
                    fechaRes = None

                if len(term) > 0:
                    if int(term) > 0:
                        oTerminoRescision = TermReason.objects.get(pk=term)
                        if not oTerminoRescision:
                            mensaje = "El término de rescisión no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(sexo) > 0:
                    if int(sexo) > 0:
                        oSex = Sex.objects.get(pk=sexo)
                        if not oSex:
                            mensaje = "El sexo no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(fecNac) == 0:
                    fecNac = None

                if len(lugNac) > 0:
                    if int(lugNac) > 0:
                        oBirthCountry = Country.objects.get(pk=lugNac)
                        if not oBirthCountry:
                            mensaje = "El lugar de nacimiento no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(estCivil) > 0:
                    if int(estCivil) > 0:
                        oCivilStatus = CivilStatus.objects.get(pk=estCivil)
                        if not oCivilStatus:
                            mensaje = "El estado civil no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(citiz) > 0:
                    if int(citiz) > 0:
                        oCitizenShip = Country.objects.get(pk=citiz)
                        if not oCitizenShip:
                            mensaje = "La nacionalidad no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
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
                            mensaje = "El tipo de salario no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(tipo_contrato) > 0:
                    if int(tipo_contrato) > 0:
                        oTipoContrato = TipoContrato.objects.get(pk=tipo_contrato)
                        if not oTipoContrato:
                            mensaje = "El tipo de contrato no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error':True
                            }
                            return JsonResponse(data)

                if len(tipo_nomina) > 0:
                    if int(tipo_nomina) > 0:
                        oTipoNomina = TipoNomina.objects.get(pk=tipo_nomina)
                        if not oTipoNomina:
                            mensaje = "El tipo de nomina no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error':True
                            }
                            return JsonResponse(data)

                if len(empCostUnit) > 0:
                    if int(empCostUnit) > 0:
                        oEmpCostUnit = CostUnit.objects.get(pk=empCostUnit)
                        if not oEmpCostUnit:
                            mensaje = "El tipo de costo de empleado no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(banco) > 0:
                    if int(banco) > 0:
                        print "LLego aqui"
                        oBankCode = Bank.objects.get(pk=banco)

                        if not oBankCode:
                            mensaje = "El banco no existe en la base de datos."
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                            return JsonResponse(data)

                if len(empCost) == 0:
                    empCost = None

                if len(salary) == 0:
                    salary = None

                if len(salario_diario) == 0:
                    salario_diario = None

                oEmp = Employee.objects.get(pk=id)
                oEmp.firstName = pNom
                oEmp.middleName = sNom
                oEmp.lastName = apellido
                oEmp.extEmpNo = no_ext
                oEmp.jobTitle = puesto
                oEmp.position = oPosicion
                oEmp.dept = oDepartamento
                oEmp.branch = oSucursal
                oEmp.jefe = oJefe
                oEmp.slsPerson = oEmpVentas
                oEmp.officeTel = telOf
                oEmp.officeExt = telExt
                oEmp.mobile = telMov
                oEmp.pager = pag
                oEmp.homeTel = telCasa
                oEmp.fax = fax
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
                oEmp.salary = salary
                oEmp.salario_diario = salario_diario
                oEmp.salaryUnits = oSalaryUnits
                oEmp.empCost = empCost
                oEmp.empCostUnit = oEmpCostUnit
                oEmp.bankCode = oBankCode
                oEmp.bankAccount = numCuenta
                oEmp.branchBank = branchBank
                oEmp.remark = remark
                oEmp.tipo_contrato = oTipoContrato
                oEmp.tipo_nomina = oTipoNomina

                oEmp.active = activo
                oEmp.user_mod = request.user
                oEmp.date_mod = datetime.datetime.now()
                oEmp.save()
                
                mensaje = 'Se ha actualizado el registro del Empleado'
                data = {
                    'mensaje':mensaje, 'error': False
                }
            else:
                mensaje = "Metodo no permitido."
                data = {
                    'mensaje':mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje':mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error':True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_empleado(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = Employee.objects.get(pk=reg_id)
                    oMd.delete()
                    mensaje = 'Se ha eliminado el registro del empleado'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    #return HttpResponseRedirect('/listar/corporativos/')
    return JsonResponse(data)

def guardar_corporativo(request):
    try:
        if  request.is_ajax():
            if request.method == 'POST':
                razon = request.POST['razon']
                nombre = request.POST['organiz']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])
                
                if len(razon) > 0:
                    oGrupo = GrupoCorporativo(
                        razonSocial = razon,
                        nombreComercial = nombre,
                        empresa_reg = suc.empresa,
                        active = activo,
                        user_reg=request.user,
                    )
                    oGrupo.save()
                    grupo = {
                        'pk':oGrupo.pk,
                        'razon':oGrupo.razonSocial,
                        'nombre':oGrupo.nombreComercial,
                        'activo':oGrupo.active,
                    }
                    mensaje = 'Se ha guardado el registro del Grupo Corporativo'
                    data = {
                        'grupo':grupo, 'mensaje':mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje':mensaje, 'error': True
                    }
            else:
                mensaje = "Metodo no permitido."
                data = {
                    'mensaje':mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje':mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error':True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_corporativo(request):
    try:
        if  request.is_ajax():
            if request.method == 'POST':
                id = request.POST['id']
                razon = request.POST['razon']
                nombre = request.POST['organiz']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(razon) > 0:
                    oGrupo = GrupoCorporativo.objects.get(pk=id)
                    #day  = timezone.now()
                    #formatedDay  = day.strftime("%Y-%m-%d %H:%M:%S")
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
                        'pk':oGrupo.pk,
                        'razon':oGrupo.razonSocial,
                        'nombre':oGrupo.nombreComercial,
                        'activo':oGrupo.active,
                    }
                    mensaje = 'Se ha actualizado el registro del Grupo Corporativo'
                    data = {
                        'grupo':grupo, 'mensaje':mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje':mensaje, 'error': True
                    }
            else:
                mensaje = "Metodo no permitido."
                data = {
                    'mensaje':mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje':mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error':True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_corporativo(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    print "Entro"
                    oGrupo = GrupoCorporativo.objects.get(pk=reg_id)
                    oGrupo.delete()
                    print "Elimino"
                    mensaje = 'Se ha eliminado el registro del Grupo Corporativo'
                    data = {
                        'mensaje':mensaje, 'error': False
                    }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error':True,
            'mensaje': 'error',
        }
    #return HttpResponseRedirect('/listar/corporativos/')
    return JsonResponse(data)

def guardar_empresa(request):
    try:
        if  request.is_ajax():
            if request.method == 'POST':
                razon = request.POST['razon']
                nombre = request.POST['organiz']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(razon) > 0:
                    oEmpresa = Empresa(
                        razonSocial = razon,
                        nombreComercial = nombre,
                        active = activo,
                        user_reg=request.user,
                    )
                    oEmpresa.save()
                    grupo = {
                        'pk':oEmpresa.pk,
                        'razon':oEmpresa.razonSocial,
                        'nombre':oEmpresa.nombreComercial,
                        'activo':oEmpresa.active,
                    }
                    mensaje = 'Se ha guardado el registro de la empresa'
                    data = {
                        'grupo':grupo, 'mensaje':mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje':mensaje, 'error': True
                    }
            else:
                mensaje = "Metodo no permitido."
                data = {
                    'mensaje':mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje':mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error':True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_empresa(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = request.POST['id']
                razon = request.POST['razon']
                nombre = request.POST['organiz']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(razon) > 0:
                    oEmp = Empresa.objects.get(pk=id)
                    if oEmp:
                        oEmp.razonSocial = razon
                        oEmp.nombreComercial = nombre
                        oEmp.active = activo
                        oEmp.user_mod = request.user
                        oEmp.date_mod = datetime.datetime.now()
                        oEmp.save()
                        emp = {
                            'pk': oEmp.pk,
                            'razon': oEmp.razonSocial,
                            'nombre': oEmp.nombreComercial,
                            'activo': oEmp.active,
                        }
                        mensaje = 'Se ha actualizado el registro de la empresa'
                        data = {
                            'emp': emp, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'El registro no existe.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Metodo no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_empresa(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oEmp = Empresa.objects.get(pk=reg_id)
                    if oEmp:
                        oEmp.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje':mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje':mensaje, 'error': False
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        data = {
            'error':True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_sucursal(request):
    try:
        if  request.is_ajax():
            if request.method == 'POST':
                nombre = request.POST['nombre']
                descripcion = request.POST['descripcion']
                activo = int(request.POST['activo'])

                if len(nombre) > 5:
                    mensaje = "El campo 'Código' tiene como máximo 6 caracteres."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(nombre) > 0:
                    oSucursal = Branch(
                        code = nombre,
                        description = descripcion,
                        active = activo,
                        user_reg=request.user,
                    )
                    oSucursal.save()
                    grupo = {
                        'pk':oSucursal.pk,
                        'nombre':oSucursal.name,
                        'descripcion':oSucursal.description,
                        'activo':oSucursal.active,
                    }
                    mensaje = 'Se ha guardado el registro de la sucursal'
                    data = {
                        'grupo':grupo, 'mensaje':mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje':mensaje, 'error': True
                    }
            else:
                mensaje = "Metodo no permitido."
                data = {
                    'mensaje':mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje':mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error':True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_sucursal(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = request.POST['id']
                nombre = request.POST['nombre']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(nombre) > 5:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)


                if len(nombre) > 0 and len(desc) > 0:
                    oSucursal = Branch.objects.get(pk=id)

                    if oSucursal:
                        oSucursal.code = nombre
                        oSucursal.description = desc
                        oSucursal.active = activo
                        oSucursal.user_mod = request.user
                        oSucursal.date_mod = datetime.datetime.now()
                        oSucursal.save()
                        sucursal = {
                            'pk': oSucursal.pk,
                            'desc': oSucursal.description,
                            'nombre': oSucursal.code,
                            'activo': oSucursal.active,
                        }
                        mensaje = 'Se ha actualizado el registro de la Sucursal'
                        data = {
                            'sucursal': sucursal, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Metodo no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_sucursal(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oSucursal = Branch.objects.get(pk=reg_id)
                    oSucursal.delete()
                    mensaje = 'Se ha eliminado el registro de la sucursal'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_division(request):
    try:
        if  request.is_ajax():
            if request.method == 'POST':
                code = request.POST['code']
                descripcion = request.POST['descripcion']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(code) > 5:
                    mensaje = "El campo 'Código' tiene un maximo de 5 caracteres."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])
                
                if len(descripcion) > 0:
                    oDivision = Divisiones(
                        code = code,
                        descripcion = descripcion,
                        empresa_reg = suc.empresa,
                        active = activo,
                        user_reg=request.user,
                    )
                    oDivision.save()
                    grupo = {
                        'pk':oDivision.pk,
                        'descripcion':oDivision.descripcion,
                        'activo':oDivision.active,
                    }
                    mensaje = 'Se ha guardado el registro de la División'
                    data = {
                        'grupo':grupo, 'mensaje':mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje':mensaje, 'error': True
                    }
            else:
                mensaje = "Metodo no permitido."
                data = {
                    'mensaje':mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje':mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error':True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_division(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = request.POST['id']
                code = request.POST['code']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oDiv = Divisiones.objects.get(pk=id)

                    if oDiv:
                        oDiv.code = code
                        oDiv.descripcion = desc
                        oDiv.active = activo
                        oDiv.user_mod = request.user
                        oDiv.date_mod = datetime.datetime.now()
                        oDiv.save()
                        division = {
                            'pk': oDiv.pk,
                            'desc': oDiv.descripcion,
                            'activo': oDiv.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'division': division, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_division(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oDivision = Divisiones.objects.get(pk=reg_id)
                    if oDivision:
                        oDivision.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_departamento(request):
    try:
        if  request.is_ajax():
            if request.method == 'POST':
                nombre = request.POST['nombre']
                descripcion = request.POST['descripcion']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(nombre) > 5:
                    mensaje = "El campo 'Código' debe ser tener como máximo 6 caracteres."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])
                
                if len(nombre) > 0 and len(descripcion) > 0:
                    oDeparment = Department(
                        code = nombre,
                        description = descripcion,
                        empresa_reg = suc.empresa,
                        active = activo,
                        user_reg=request.user,
                    )
                    oDeparment.save()
                    grupo = {
                        'pk':oDeparment.pk,
                        'codigo':oDeparment.code,
                        'descripcion':oDeparment.description,
                        'activo':oDeparment.active,
                    }
                    mensaje = 'Se ha guardado el registro del Departamento'
                    data = {
                        'grupo':grupo, 'mensaje':mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje':mensaje, 'error': True
                    }
            else:
                mensaje = "Metodo no permitido."
                data = {
                    'mensaje':mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje':mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error':True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_departamento(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = request.POST['id']
                nombre = request.POST['nombre']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oDep = Department.objects.get(pk=id)

                    if oDep:
                        oDep.code = nombre
                        oDep.description = desc
                        oDep.active = activo
                        oDep.user_mod = request.user
                        oDep.date_mod = datetime.datetime.now()
                        oDep.save()
                        dep = {
                            'pk': oDep.pk,
                            'name':oDep.code,
                            'desc': oDep.description,
                            'activo': oDep.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'departamento': dep, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_departamento(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oDivision = Department.objects.get(pk=reg_id)
                    totReg = Employee.objects.filter(dept__pk=reg_id).count()
                    if oDivision:
                        if totReg == 0:
                            oDivision.delete()
                            mensaje = 'Se ha eliminado el registro.'
                            data = {
                                'mensaje': mensaje, 'error': False
                            }
                        else:
                            mensaje = 'Existen datos asociados al registro que quiere eliminar.'
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_puesto(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                nombre = request.POST['nombre']
                descripcion = request.POST['descripcion']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(nombre) > 5:
                    data = {
                        'error': True,
                        'mensaje': 'El campo "Código" debe tener un máximo de 5 caracteres.',
                    }
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])
                if len(nombre) > 0 and len(descripcion) > 0:
                    oPuesto = Position(
                        code=nombre,
                        description=descripcion,
                        empresa_reg=suc.empresa,
                        active=activo,
                        user_reg=request.user,
                    )
                    oPuesto.save()
                    grupo = {
                        'pk': oPuesto.pk,
                        'descripcion': oPuesto.description,
                        'activo': oPuesto.active,
                    }
                    mensaje = 'Se ha guardado el registro del Puesto de Trabajo'
                    data = {
                        'grupo': grupo, 'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Metodo no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_puesto(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                nombre = request.POST['nombre']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(nombre) > 5:
                    data = {
                        'error': True,
                        'mensaje': 'El campo "Código" debe tener un máximo de 5 caracteres.',
                    }
                    return JsonResponse(data)
                
                
                if len(nombre) > 0 and len(desc) > 0:
                    oPos = Position.objects.get(pk=id)

                    if oPos:
                        oPos.code = nombre
                        oPos.description = desc
                        oPos.active = activo
                        oPos.user_mod = request.user
                        oPos.date_mod = datetime.datetime.now()
                        oPos.save()
                        pos = {
                            'pk': oPos.pk,
                            'name':oPos.code,
                            'desc': oPos.description,
                            'activo': oPos.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'puesto': pos, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_puesto(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oPuesto = Position.objects.get(pk=reg_id)
                    totReg = Employee.objects.filter(dept__pk=reg_id).count()
                    if oPuesto:
                        if totReg == 0:
                            oPuesto.delete()
                            mensaje = 'Se ha eliminado el registro.'
                            data = {
                                'mensaje': mensaje, 'error': False
                            }
                        else:
                            mensaje = 'Existen datos asociados al registro que quiere eliminar.'
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_ccosto(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                code = request.POST['code']
                descripcion = request.POST['descripcion']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(code) > 5:
                    mensaje = 'El campo "Código" tiene un máximo de 5 caracteres'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])

                if len(descripcion) > 0:
                    oCCosto = CentrosCostos(
                        code = code,
                        descripcion=descripcion,
                        empresa_reg = suc.empresa,
                        active=activo,
                        user_reg=request.user,
                    )
                    oCCosto.save()
                    grupo = {
                        'pk': oCCosto.pk,
                        'descripcion': oCCosto.descripcion,
                        'activo': oCCosto.active,
                    }
                    mensaje = 'Se ha guardado el registro del Centro de Costos'
                    data = {
                        'grupo': grupo, 'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_ccosto(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                code = request.POST['code']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(desc) > 0:
                    oCC = CentrosCostos.objects.get(pk=id)

                    if oCC:
                        oCC.descripcion = desc
                        oCC.code = code
                        oCC.active = activo
                        oCC.user_mod = request.user
                        oCC.date_mod = datetime.datetime.now()
                        oCC.save()
                        CC = {
                            'pk': oCC.pk,
                            'desc': oCC.descripcion,
                            'activo': oCC.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'puesto': CC, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_ccosto(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oCC = CentrosCostos.objects.get(pk=reg_id)
                    if oCC:
                        oCC.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_pais(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                codigo = request.POST['codigo']
                nombre = request.POST['nombre']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                if len(nombre) > 0 and len(codigo) > 0:
                    oCountry = Country(
                        code = codigo,
                        name = nombre,
                        empresa_reg = suc.empresa,
                        active=activo,
                        user_reg=request.user,
                    )
                    oCountry.save()
                    grupo = {
                        'pk': oCountry.pk,
                        'codigo': oCountry.code,
                        'name': oCountry.name,
                        'activo': oCountry.active,
                    }
                    mensaje = 'Se ha guardado el registro del País'
                    data = {
                        'grupo': grupo, 'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_pais(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                cod = request.POST['codigo']
                nombre = request.POST['nombre']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(cod) > 0 and len(nombre) > 0:
                    oCoun = Country.objects.get(pk=id)
                    if oCoun:
                        oCoun.code = cod
                        oCoun.name = nombre
                        oCoun.active = activo
                        oCoun.user_mod = request.user
                        oCoun.date_mod = datetime.datetime.now()
                        oCoun.save()
                        country = {
                            'pk': oCoun.pk,
                            'codigo':oCoun.code,
                            'nombre': oCoun.name,
                            'activo': oCoun.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'puesto': country, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_pais(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oC = Country.objects.get(pk=reg_id)
                    totReg = Employee.objects.filter(homeCountry__id=reg_id).count()
                    totReg += Employee.objects.filter(workCountry__id=reg_id).count()
                    totReg += Employee.objects.filter(birthCountry__id=reg_id).count()
                    totReg += Employee.objects.filter(citizenship__id=reg_id).count()
                    if oC:
                        if totReg == 0:
                            oC.delete()
                            mensaje = 'Se ha eliminado el registro.'
                            data = {
                                'mensaje': mensaje, 'error': False
                            }
                        else:
                            mensaje = 'El registro tiene datos asociados.'
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_deptos(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                codigo = request.POST['codigo']
                nombre = request.POST['nombre']
                pais = request.POST['pais']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(codigo) == 0:
                    mensaje = "El campo 'Código' es obligatorio."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(codigo) > 5:
                    mensaje = "El campo 'Código' tiene como máximo 5 caracteres."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if pais == 0:
                    mensaje = "El campo 'País' es obligatorio."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])
                pais = Country.objects.get(pk=pais)

                if len(nombre) > 0 and len(codigo) > 0:
                    oDepto = State(
                        code = codigo,
                        name = nombre,
                        empresa_reg = suc.empresa,
                        active=activo,
                        pais = pais,
                        user_reg=request.user,
                    )
                    oDepto.save()
                    grupo = {
                        'pk': oDepto.pk,
                        'code': oDepto.code,
                        'name': oDepto.name,
                        'activo': oDepto.active,
                    }
                    mensaje = 'Se ha guardado el registro'
                    data = {
                        'grupo': grupo, 'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_deptos(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                cod = request.POST['codigo']
                pais = request.POST['pais']
                nombre = request.POST['nombre']
                activo = int(request.POST['activo'])

                if pais == 0:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                pais = Country.objects.get(pk=pais)
                
                if len(cod) > 0 and len(nombre) > 0:
                    oDept = State.objects.get(pk=id)
                    if oDept:
                        oDept.code = cod
                        oDept.name = nombre
                        oDept.pais = pais
                        oDept.active = activo
                        oDept.user_mod = request.user
                        oDept.date_mod = datetime.datetime.now()
                        oDept.save()
                        estado = {
                            'pk': oDept.pk,
                            'codigo':oDept.code,
                            'nombre': oDept.name,
                            'activo': oDept.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'puesto': estado, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_depto(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oS = State.objects.get(pk=reg_id)
                    totReg = Employee.objects.filter(homeState__id=reg_id).count()
                    totReg += Employee.objects.filter(workState__id=reg_id).count()
                    if oS:
                        if totReg == 0:
                            oS.delete()
                            mensaje = 'Se ha eliminado el registro.'
                            data = {
                                'mensaje': mensaje, 'error': False
                            }
                        else:
                            mensaje = 'El registro tiene datos asociados.'
                            data = {
                                'mensaje': mensaje, 'error': True
                            }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_ciudades(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                ID = request.POST['ID']
                nombre = request.POST['nombre']
                activo = int(request.POST['activo'])

                if len(ID) > 5:
                    mensaje = "El campo 'Código' tiene un máximo de 5 caracteres."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                if len(nombre) > 0 and len(ID) > 0:
                    oCdd = Ciudad(
                        code = ID,
                        nombre = nombre,
                        empresa_reg = suc.empresa,
                        active=activo,
                        user_reg=request.user,
                    )
                    oCdd.save()
                    ciudad = {
                        'pk': oCdd.pk,
                        'ID': oCdd.code,
                        'nombre': oCdd.nombre,
                        'activo': oCdd.active,
                    }
                    mensaje = 'Se ha guardado el registro'
                    data = {
                        'grupo': ciudad, 'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_ciudad(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                ID = request.POST['ID']
                nombre = request.POST['nombre']
                activo = int(request.POST['activo'])

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
                        oCdd.date_mod = datetime.datetime.now()
                        oCdd.save()
                        ciudad = {
                            'pk': oCdd.pk,
                            'ID':oCdd.code,
                            'nombre': oCdd.nombre,
                            'activo': oCdd.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'ciudad': ciudad, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_ciudad(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oCdd = Ciudad.objects.get(pk=reg_id)
                    if oCdd:
                        oCdd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_genero(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                code = request.POST['code']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                if len(desc) > 0:
                    oGnr = Sex(
                        code = code,
                        description = desc,
                        empresa_reg = suc.empresa,
                        active=activo,
                        user_reg=request.user,
                    )
                    oGnr.save()
                    genero = {
                        'pk': oGnr.pk,
                        'code': oGnr.code,
                        'desc': oGnr.description,
                        'activo': oGnr.active,
                    }
                    mensaje = 'Se ha guardado el registro'
                    data = {
                        'generos': genero, 'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_genero(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                desc = request.POST['desc']
                code = request.POST['code']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(desc) > 0:
                    oGnr = Sex.objects.get(pk=id)
                    if oGnr:
                        oGnr.code = code
                        oGnr.description = desc
                        oGnr.active = activo
                        oGnr.user_mod = request.user
                        oGnr.date_mod = datetime.datetime.now()
                        oGnr.save()
                        genero = {
                            'pk': oGnr.pk,
                            'desc': oGnr.description,
                            'activo': oGnr.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'ciudad': genero, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_genero(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oGnr = Sex.objects.get(pk=reg_id)
                    if oGnr:
                        totReg = Employee.objects.filter(sex__id=reg_id).count()
                        if totReg == 0:
                            oGnr.delete()
                            mensaje = 'Se ha eliminado el registro.'
                            data = {
                                'mensaje': mensaje, 'error': False
                            }
                        else:
                            mensaje = 'El registro tiene datos asociados.'
                            data = {
                                'mensaje': mensaje, 'error': False
                            }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_estado_civil(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                desc = request.POST['desc']
                code = request.POST['code']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(code) > 5:
                    mensaje = "El campo 'Código' tiene como máximo 6 caracteres."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }

                suc = Branch.objects.get(pk=request.session["sucursal"])

                if len(desc) > 0:
                    oCv = CivilStatus(
                        code = code,
                        description = desc,
                        empresa_reg = suc.empresa,
                        active=activo,
                        user_reg=request.user,
                    )
                    oCv.save()
                    estado = {
                        'pk': oCv.pk,
                        'desc': oCv.description,
                        'activo': oCv.active,
                    }
                    mensaje = 'Se ha guardado el registro'
                    data = {
                        'estado': estado, 'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_estado_civil(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                code = request.POST['code']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(desc) > 0:
                    oCV = CivilStatus.objects.get(pk=id)
                    if oCV:
                        oCV.code = code
                        oCV.description = desc
                        oCV.active = activo
                        oCV.user_mod = request.user
                        oCV.date_mod = datetime.datetime.now()
                        oCV.save()
                        estado = {
                            'pk': oCV.pk,
                            'desc': oCV.description,
                            'activo': oCV.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'estado': estado, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_estado_civil(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oCV = CivilStatus.objects.get(pk=reg_id)
                    if oCV:
                        totReg = Employee.objects.filter(marrStatus__id=reg_id).count()
                        if totReg == 0:
                            oCV.delete()
                            mensaje = 'Se ha eliminado el registro.'
                            data = {
                                'mensaje': mensaje, 'error': False
                            }
                        else:
                            mensaje = 'El registro tiene datos asociados.'
                            data = {
                                'mensaje': mensaje, 'error': False
                            }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_parentesco(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                desc = request.POST['desc']
                code = request.POST['code']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(code) > 5:
                    mensaje = "El campo 'código' tiene como máximo 6 caracteres."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])

                if len(desc) > 0:
                    oPr = Parentesco(
                        descripcion = desc,
                        code = code,
                        empresa_reg = suc.empresa,
                        active=activo,
                        user_reg=request.user,
                    )
                    oPr.save()
                    parentesco = {
                        'pk': oPr.pk,
                        'desc': oPr.descripcion,
                        'activo': oPr.active,
                    }
                    mensaje = 'Se ha guardado el registro'
                    data = {
                        'parentesco': parentesco, 'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_parentesco(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                desc = request.POST['desc']
                code = request.POST['code']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(desc) > 0:
                    oPr = Parentesco.objects.get(pk=id)
                    if oPr:
                        oPr.code = code
                        oPr.descripcion = desc
                        oPr.active = activo
                        oPr.user_mod = request.user
                        oPr.date_mod = datetime.datetime.now()
                        oPr.save()
                        parentesco = {
                            'pk': oPr.pk,
                            'desc': oPr.descripcion,
                            'activo': oPr.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'parentesco': parentesco, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_parentesco(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oPr = Parentesco.objects.get(pk=reg_id)
                    if oPr:
                        oPr.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_funciones(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                desc = request.POST['desc']
                code = request.POST['code']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(code) > 5:
                    mensaje = "El campo 'Código' tiene como máximo 5 caracteres."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])

                if len(desc) > 0:
                    oFn = FuncionesTrabajo(
                        descripcion = desc,
                        code = code,
                        empresa_reg = suc.empresa,
                        active=activo,
                        user_reg=request.user,
                    )
                    oFn.save()
                    funcion = {
                        'pk': oFn.pk,
                        'code': oFn.code,
                        'desc': oFn.descripcion,
                        'activo': oFn.active,
                    }
                    mensaje = 'Se ha guardado el registro'
                    data = {
                        'funcion': funcion, 'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_funcion(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                code = request.POST['code']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(desc) > 0:
                    oFn = FuncionesTrabajo.objects.get(pk=id)
                    if oFn:
                        oFn.code = code
                        oFn.descripcion = desc
                        oFn.active = activo
                        oFn.user_mod = request.user
                        oFn.date_mod = datetime.datetime.now()
                        oFn.save()
                        funcion = {
                            'pk': oFn.pk,
                            'code':oFn.code,
                            'desc': oFn.descripcion,
                            'activo': oFn.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'funcion': funcion, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_funcion_trabajo(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oFn = FuncionesTrabajo.objects.get(pk=reg_id)
                    if oFn:
                        oFn.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_equipos(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                code = request.POST['code']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0 and len(code) > 0:
                    if len(code) > 5:
                        mensaje = "El campo 'código' tiene como máximo 5 caracteres."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                    suc = Branch.objects.get(pk=request.session["sucursal"])

                    oEq = EquipoTrabajo(
                        code = code,
                        descripcion = desc,
                        empresa_reg = suc.empresa,
                        active=activo,
                        user_reg=request.user,
                    )
                    oEq.save()
                    equipo = {
                        'pk': oEq.pk,
                        'code': oEq.code,
                        'desc': oEq.descripcion,
                        'activo': oEq.active,
                    }
                    mensaje = 'Se ha guardado el registro'
                    data = {
                        'equipo': equipo, 'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_equipos(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                code = request.POST['code']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if len(code) > 5:
                    mensaje = "El campo 'Código' tiene como máximo 5 caracteres."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(desc) > 0:
                    oMd = EquipoTrabajo.objects.get(pk=id)
                    if oMd:
                        oMd.code = code
                        oMd.descripcion = desc
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        registro = {
                            'pk': oMd.pk,
                            'code':oMd.code,
                            'desc': oMd.descripcion,
                            'activo': oMd.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'registro': registro, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_equipo_trabajo(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = EquipoTrabajo.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_estado_empleado(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                nombre = request.POST['nombre']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if len(nombre):
                    mensaje = "El campo 'Código' tiene como maximo 5 caracteres."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0 and len(nombre) > 0:
                    oMd = StatusEmp(
                        code = nombre,
                        description = desc,
                        active=activo,
                        user_reg=request.user,
                    )
                    oMd.save()
                    registro = {
                        'pk': oMd.pk,
                        'nombre': oMd.code,
                        'desc': oMd.description,
                        'activo': oMd.active,
                    }
                    mensaje = 'Se ha guardado el registro'
                    data = {
                        'registro': registro, 'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_estatus_empleado(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                nombre = request.POST['nombre']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(desc) > 0 and len(nombre) > 0:
                    oMd = StatusEmp.objects.get(pk=id)
                    if oMd:
                        oMd.code = nombre
                        oMd.description = desc
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        registro = {
                            'pk': oMd.pk,
                            'nombre':oMd.code,
                            'desc': oMd.description,
                            'activo': oMd.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'registro': registro, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_estatus_empleado(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = StatusEmp.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_ausentismo(request):
    oEmp = None
    oAprobo = None
    try:
        if request.is_ajax():
            if request.method == 'POST':
                emp = request.POST['emp']
                desde = request.POST['desde']
                hasta = request.POST['hasta']
                motivo = request.POST['motivo']
                aprobo = request.POST['aprobo']
                activo = request.POST['activo']
                
                if len(emp) == 0:
                    mensaje = 'Seleccione un empleado.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    else:
                        mensaje = 'Seleccione un empleado.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                if len(desde) == 0:
                    mensaje = "Ingrese una fecha válida en el campo 'Desde'."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(hasta) == 0:
                    mensaje = "Ingrese una fecha válida en el campo 'Hasta'."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(motivo) == 0:
                    mensaje = 'Seleccione un motivo por ausencia.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(motivo) > 0:
                        oMot = MotivosAusencia.objects.get(pk=motivo)
                    else:
                        mensaje = 'Seleccione un motivo por ausencia.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                if len(aprobo) == 0:
                    mensaje = 'Seleccione el empleado que Aprobó.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(aprobo) > 0:
                        oAprobo = Employee.objects.get(pk=aprobo)

                if int(emp) == int(aprobo):
                    mensaje = 'El empleado debe ser distinto al usuario que apruebe.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)



                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = Ausentismo(
                    empleado = oEmp,
                    desde = desde,
                    hasta = hasta,
                    motivo = oMot,
                    aprobado = oAprobo,
                    empresa_reg = suc.empresa,
                    sucursal_reg = suc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    'pk': oMd.pk,
                    'empleado': oMd.empleado.pk,
                    'desde': oMd.desde,
                    'hasta': oMd.hasta,
                    'motivo': oMd.motivo.pk,
                    'activo': oMd.active,
                }
                mensaje = 'Se ha guardado el registro'
                data = {
                    'registro': registro, 'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_ausentismo(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                emp = request.POST['emp']
                desde = request.POST['desde']
                hasta = request.POST['hasta']
                motivo = request.POST['motivo']
                aprobo = request.POST['aprobo']
                activo = int(request.POST['activo'])
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
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                if len(desde) == 0:
                    mensaje = "Ingrese un valor válido en campo 'Desde'."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                
                if len(hasta) == 0:
                    mensaje = "Ingrese un valor válido en campo 'Hasta'."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(motivo) == 0:
                    mensaje = 'Seleccione un motivo por ausencia.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(motivo) > 0:
                        oMot = MotivosAusencia.objects.get(pk=motivo)
                    else:
                        mensaje = 'Seleccione un motivo por ausencia.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                if int(emp) == int(aprobo):
                    mensaje = 'El empleado debe ser distinto al usuario que apruebe.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                print oEmp
                
                oMd = Ausentismo.objects.get(pk=id)
                if oMd:
                    oMd.empleado = oEmp
                    oMd.desde = desde
                    oMd.hasta = hasta
                    oMd.motivo = oMot
                    oMd.aprobado = oApro
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    registro = {
                        'pk': oMd.pk,
                        'empleado':oMd.empleado.pk,
                        'desde': oMd.desde,
                        'hasta': oMd.hasta,
                        'motivo': oMd.motivo,
                        'activo': oMd.active,
                    }
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'registro': registro, 'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_ausentismo(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = Ausentismo.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_motivo_ausencia(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                desc = request.POST['desc']
                code = request.POST['code']
                pagado = request.POST['pagado']
                activo = request.POST['activo']
                
                if len(desc) == 0:
                    mensaje = 'Ingrese una descripción.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = 'El campo "Código" tiene como máximo 5 caracteres.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
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

                oMd = MotivosAusencia(
                    code = code,
                    descripcion = desc,
                    pagado = pagado,
                    empresa_reg = suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    'pk': oMd.pk,
                    'desc': oMd.descripcion,
                    'pagado': oMd.pagado,
                    'activo': oMd.active,
                }
                mensaje = 'Se ha guardado el registro'
                data = {
                    'registro': registro, 'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_motivo_ausencia(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                code = request.POST['code']
                desc = request.POST['desc']
                pagado = request.POST['pagado']
                activo = int(request.POST['activo'])

                if int(pagado) == 1:
                    pagado = True
                else:
                    pagado = False

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(desc) > 0:
                    oMd = MotivosAusencia.objects.get(pk=id)
                    if oMd:
                        oMd.descripcion = desc
                        oMd.code = code
                        oMd.pagado = pagado
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        registro = {
                            'pk': oMd.pk,
                            'descripcion':oMd.descripcion,
                            'pagado': oMd.pagado,
                            'activo': oMd.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'registro': registro, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_motivo_ausencia(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = MotivosAusencia.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_motivo_despido(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                desc = request.POST['desc']
                code = request.POST['code']
                activo = request.POST['activo']
                
                if len(code) == 0:
                    mensaje = 'El campo "Código" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = 'El campo "Código" tiene como máximo 5 caracteres.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = MotivosDespido(
                    descripcion = desc,
                    empresa_reg=suc.empresa,
                    code = code,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    'pk': oMd.pk,
                    'desc': oMd.descripcion,
                    'code': oMd.code,
                    'activo': oMd.active,
                }
                mensaje = 'Se ha guardado el registro'
                data = {
                    'registro': registro, 'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_motivo_despido(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                desc = request.POST['desc']
                code = request.POST['code']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(desc) > 0:
                    oMd = MotivosDespido.objects.get(pk=id)
                    if oMd:
                        oMd.descripcion = desc
                        oMd.code = code
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        registro = {
                            'pk': oMd.pk,
                            'descripcion':oMd.descripcion,
                            'code': oMd.code,
                            'activo': oMd.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'registro': registro, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_motivo_despido(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = MotivosDespido.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_motivo_renuncia(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                desc = request.POST['desc']
                code = request.POST['code']
                activo = request.POST['activo']

                if len(code) == 0:
                    mensaje = 'El campo "Código" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                
                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = 'El campo "Código" tiene como máximo 5 caracteres.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                oMd = MotivosRenuncia(
                    code = code,
                    descripcion = desc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    'pk': oMd.pk,
                    'code': oMd.code,
                    'desc': oMd.descripcion,
                    'activo': oMd.active,
                }
                mensaje = 'Se ha guardado el registro'
                data = {
                    'registro': registro, 'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_motivo_renuncia(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                code = request.POST['code']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if len(code) == 0:
                    mensaje = 'El campo "Código" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = 'El campo "Código" tiene como máximo 5 caracteres.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(desc) > 0:
                    oMd = MotivosRenuncia.objects.get(pk=id)
                    if oMd:
                        oMd.code = code
                        oMd.descripcion = desc
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        registro = {
                            'pk': oMd.pk,
                            'code': oMd.code,
                            'descripcion':oMd.descripcion,
                            'activo': oMd.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'registro': registro, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_motivo_renuncia(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = MotivosRenuncia.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_clase_educacion(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                code = request.POST['code']
                desc = request.POST['desc']
                activo = request.POST['activo']

                if len(code) == 0:
                    mensaje = 'El campo "Código" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                
                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = 'El campo "Código" es tiene como máximo 5 caracteres.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = ClaseEducacion(
                    code =code,
                    descripcion = desc,
                    empresa_reg = suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    'pk': oMd.pk,
                    'codigo': oMd.code,
                    'desc': oMd.descripcion,
                    'activo': oMd.active,
                }
                mensaje = 'Se ha guardado el registro'
                data = {
                    'registro': registro, 'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_clase_educacion(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                desc = request.POST['desc']
                code = request.POST['code']
                activo = int(request.POST['activo'])

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
                            'pk': oMd.pk,
                            'code':oMd.code,
                            'descripcion':oMd.descripcion,
                            'activo': oMd.active,
                        }
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'registro': registro, 'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_clase_educacion(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = ClaseEducacion.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_educacion(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                emp = request.POST['emp']
                formacion = request.POST['formacion']
                desde = request.POST['desde']
                hasta = request.POST['hasta']
                entidad = request.POST['entidad']
                asignatura = request.POST['asignatura']
                titulo = request.POST['titulo']

                if len(emp) == 0:
                    mensaje = 'Seleccione un empleado.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    else:
                        mensaje = 'Seleccione un empleado.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                if len(formacion) == 0:
                    mensaje = 'Seleccione una Clase de Formación.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(formacion) > 0:
                        oClsEdu = ClaseEducacion.objects.get(pk=formacion)
                    else:
                        mensaje = 'Seleccione una Clase de Formación.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                if len(desde) == 0:
                    mensaje = 'El campo "Desde" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                
                if len(hasta) == 0:
                    mensaje = 'El campo "Hasta" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(entidad) == 0:
                    mensaje = 'El campo "Institución" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(asignatura) == 0:
                    mensaje = 'El campo "Asignatura Principal" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(titulo) == 0:
                    mensaje = 'El campo "Título" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = Educacion(
                    empleado = oEmp,
                    clase_edu = oClsEdu,
                    desde = desde,
                    hasta = hasta,
                    entidad = entidad,
                    asignatura_principal = asignatura,
                    titulo = titulo,
                    empresa_reg = suc.empresa,
                    active=True,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    'pk': oMd.pk,
                    'emp': oMd.empleado.pk,
                    'clase_edu': oMd.clase_edu.pk,
                    'desde': oMd.desde,
                    'hasta': oMd.hasta,
                    'entidad': oMd.entidad,
                    'asignatura': oMd.asignatura_principal,
                    'titulo': oMd.titulo,
                    'activo': oMd.active,
                }
                mensaje = 'Se ha guardado el registro'
                data = {
                    'registro': registro, 'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_educacion(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                emp = request.POST['emp']
                formacion = request.POST['formacion']
                desde = request.POST['desde']
                hasta = request.POST['hasta']
                entidad = request.POST['entidad']
                asignatura = request.POST['asignatura']
                titulo = request.POST['titulo']

                if len(emp) == 0:
                    mensaje = 'Seleccione un empleado.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    else:
                        mensaje = 'Seleccione un empleado.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                if len(formacion) == 0:
                    mensaje = 'Seleccione una Clase de Formación.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(formacion) > 0:
                        oClsEdu = ClaseEducacion.objects.get(pk=formacion)
                    else:
                        mensaje = 'Seleccione una Clase de Formación.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                if len(desde) == 0:
                    mensaje = 'El campo "Desde" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                
                if len(hasta) == 0:
                    mensaje = 'El campo "Hasta" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(entidad) == 0:
                    mensaje = 'El campo "Institución" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(asignatura) == 0:
                    mensaje = 'El campo "Asignatura Principal" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(titulo) == 0:
                    mensaje = 'El campo "Título" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                
                oMd = Educacion.objects.get(pk=id)
                print "Valor empleado en educacion: " + str(oEmp)
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
                        'pk': oMd.pk,
                        'empleado':oMd.empleado.pk,
                        'clase_educacion':oMd.clase_edu.pk,
                        'desde': oMd.desde,
                        'hasta': oMd.hasta,
                        'entidad': oMd.entidad,
                        'asignatura': oMd.asignatura_principal,
                        'titulo': oMd.titulo,
                    }
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'registro': registro, 'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_educacion(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = Educacion.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_evaluacion(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                emp = request.POST['emp']
                gerente = request.POST['gerente']
                fecha = request.POST['fecha']
                grupo_asal = request.POST['grupo_asal']
                desc = request.POST['desc']
                coment = request.POST['coment']
                oGerente = None

                if len(emp) == 0:
                    mensaje = 'Seleccione un empleado.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    elif int(emp) == 0:
                        mensaje = 'Seleccione un empleado.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)
                    else:
                        mensaje = 'Empleado no existe.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                if len(gerente) > 0:
                    if int(gerente) > 0:
                        oGerente = Employee.objects.get(pk=gerente)

                if int(emp) == int(gerente):
                    data = {
                        'mensaje':'El campo empleado no puede ser la misma opción que el gerente.',
                        'error':True,
                    }
                    return JsonResponse(data)


                if len(fecha) == 0:
                    mensaje = 'El campo "Fecha" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(grupo_asal) == 0:
                    mensaje = 'El campo "Grupo asalariado" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(coment) == 0:
                    mensaje = 'El campo "Comentario" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                suc = Branch.objects.get(pk=request.session["sucursal"])


                oMd = Evaluacion(
                    empleado=oEmp,
                    gerente=oGerente,
                    fecha=fecha,
                    grupo_salarial=grupo_asal,
                    descripcion=desc,
                    comentario=coment,
                    empresa_reg = suc.empresa,
                    active=True,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_evaluacion(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                emp = request.POST['emp']
                gerente = request.POST['gerente']
                fecha = request.POST['fecha']
                grupo_asal = request.POST['grupo_asal']
                desc = request.POST['desc']
                coment = request.POST['coment']

                if len(emp) == 0:
                    mensaje = 'Seleccione un empleado.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    elif int(emp) == 0:
                        mensaje = 'Seleccione un empleado.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)
                    else:
                        mensaje = 'Empleado no existe.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                if len(gerente) > 0:
                    if int(gerente) > 0:
                        oGerente = Employee.objects.get(pk=gerente)

                if int(emp) == int(gerente):
                    data = {
                        'mensaje': 'El campo empleado no puede ser la misma opción que el gerente.',
                        'error': True,
                    }
                    return JsonResponse(data)

                if len(fecha) == 0:
                    mensaje = 'El campo "Fecha" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(grupo_asal) == 0:
                    mensaje = 'El campo "Grupo asalariado" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(coment) == 0:
                    mensaje = 'El campo "Comentario" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                oEmple = Employee.objects.get(pk=emp)
                oGerent = Employee.objects.get(pk=gerente)
                oMd = Evaluacion.objects.get(pk=id)
                print "Valor empleado: " + str(oEmple)
                if oMd:
                    oMd.empleado = oEmple,
                    oMd.gerente = oGerent,
                    oMd.fecha = fecha,
                    oMd.grupo_salarial = grupo_asal,
                    oMd.descripcion = desc,
                    oMd.comentario = coment,
                    oMd.active = True,
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_evaluacion(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = Evaluacion.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_motivo_aumento_sueldo(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                desc = request.POST['desc']
                code = request.POST['code']
                activo = request.POST['activo']

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(code) == 0:
                    mensaje = 'El campo "Código" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(code) > 5:
                    mensaje = 'El campo "Código" tiene como máximo 5 caracteres.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = MotivoAumentoSueldo(
                    code = code,
                    descripcion=desc,
                    empresa_reg = suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_motivo_aumento_sueldo(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                desc = request.POST['desc']
                code = request.POST['code']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oMd = MotivoAumentoSueldo.objects.get(pk=id)
                    if oMd:
                        oMd.descripcion = desc
                        oMd.code = code
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_motivo_aumento_sueldo(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = MotivoAumentoSueldo.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_motivo_rescision_contrato(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                nombre = request.POST['nombre']
                desc = request.POST['desc']
                activo = request.POST['activo']

                if len(nombre) == 0:
                    mensaje = 'El campo "código" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(nombre) > 5:
                    mensaje = 'El campo "código" tiene como máximo de 5 caracteres.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = TermReason(
                    code = nombre,
                    description=desc,
                    empresa_reg=suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_motivo_rescision_contrato(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                desc = request.POST['desc']
                nombre = request.POST['nombre']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oMd = TermReason.objects.get(pk=id)
                    if oMd:
                        oMd.description = desc
                        oMd.code = nombre
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        mensaje = 'Se ha actualizado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = "No existe el registro."
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_motivo_rescision_contrato(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = TermReason.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_empleo_anterior(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                emp = request.POST['emp']
                desde = request.POST['desde']
                hasta = request.POST['hasta']
                empresa = request.POST['empresa']
                posicion = request.POST['posicion']
                comentario = request.POST['comentario']
                activo = request.POST['activo']

                if len(emp) == 0:
                    mensaje = 'Seleccione un empleado.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    elif int(emp) == 0:
                        mensaje = 'Seleccione un empleado.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)
                    else:
                        mensaje = 'Empleado no existe.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                if len(desde) == 0:
                    mensaje = 'El campo "Desde" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(hasta) == 0:
                    mensaje = 'El campo "Hasta" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(empresa) == 0:
                    mensaje = 'El campo "Empresa" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(posicion) == 0:
                    mensaje = 'El campo "Posición" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                oMd = EmpleosAnteriores(
                    empleado = oEmp,
                    desde = desde,
                    hasta = hasta,
                    empresa = empresa,
                    posicion = posicion,
                    comentario = comentario,
                    user_reg=request.user,
                    active= activo,
                )
                oMd.save()
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_empleo_anterior(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                emp = request.POST['emp']
                desde = request.POST['desde']
                hasta = request.POST['hasta']
                empresa = request.POST['empresa']
                posicion = request.POST['posicion']
                comentario = request.POST['comentario']
                activo = request.POST['activo']
                oEmp = None

                if len(emp) == 0:
                    mensaje = 'Seleccione un empleado.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    elif int(emp) == 0:
                        mensaje = 'Seleccione un empleado.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)
                    else:
                        mensaje = 'Empleado no existe.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                if len(desde) == 0:
                    mensaje = 'El campo "Desde" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(hasta) == 0:
                    mensaje = 'El campo "Hasta" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(empresa) == 0:
                    mensaje = 'El campo "Empresa" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if len(posicion) == 0:
                    mensaje = 'El campo "Posición" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
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
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_empleo_anterior(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = EmpleosAnteriores.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_grupo_comision(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                desc = request.POST['desc']
                code = request.POST['code']
                activo = request.POST['activo']

                if len(code) == 0:
                    mensaje = 'El campo "Código" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 
                        'error':False,
                    }

                if len(desc) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 
                        'error':False,
                    }

                if len(code) == 0:
                    mensaje = 'El campo "Código" tiene como máximo 5 caracteres.'
                    data = {
                        'mensaje': mensaje,
                        'error': False,
                    }

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = GrupoComisiones(
                    descripcion=desc,
                    code = code,
                    empresa_reg = suc.empresa,
                    active=True,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_grupo_comision(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                desc1 = request.POST['desc']
                activo1 = request.POST['activo']
                acti = False

                if len(desc1) == 0:
                    mensaje = 'El campo "Descripción" es obligatorio.'
                    data = {
                        'mensaje': mensaje,
                        'error': False,
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
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_grupo_comision(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = GrupoComisiones.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_vendedor(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                nombre = request.POST['nombre']
                grp_com = request.POST['grupo_com']
                porcent = request.POST['porcentaje']
                emp = request.POST['emp']
                tel = request.POST['tel']
                movil = request.POST['movil']
                correo = request.POST['correo']
                coment = request.POST['coment']
                activo = int(request.POST['activo'])
                oGrpCom = None
                vPorcentajeComision = 0

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre' es obligatorio."
                    data = {'error':True, 'mensaje':mensaje}
                    return JsonResponse(data)

                if len(grp_com) == 0:
                    mensaje = "El campo 'Grupo de Comisión' es obligatorio."
                    data = {'error':True, 'mensaje':mensaje}
                    return JsonResponse(data)
                else:
                    if int(grp_com) > 0:
                        oGrpCom = GrupoComisiones.objects.get(pk=grp_com)

                if len(porcent) > 0:
                    vPorcentajeComision = porcent

                if len(emp) == 0:
                    mensaje = 'Seleccione un empleado.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    elif int(emp) == 0:
                        mensaje = 'Seleccione un empleado.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)
                    else:
                        mensaje = 'Empleado no existe.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)


                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = Vendedor(
                    nombre=nombre,
                    grupo_comisiones=oGrpCom,
                    porcentaje_comision=float(vPorcentajeComision),
                    empleado=oEmp,
                    telefono = tel,
                    tel_movil = movil,
                    correo = correo,
                    comentario = coment,
                    empresa_reg = suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_vendedor(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                nombre = request.POST['nombre']
                grp_com = request.POST['grupo_com']
                porcent = request.POST['porcentaje']
                emp = request.POST['emp']
                tel = request.POST['tel']
                movil = request.POST['movil']
                correo = request.POST['correo']
                coment = request.POST['coment']
                activo = int(request.POST['activo'])
                vPorcentajeComision = 0.00

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(grp_com) == 0:
                    mensaje = "El campo 'Grupo de Comisión' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)
                else:
                    if int(grp_com) > 0:
                        oGrpCom = GrupoComisiones.objects.get(pk=grp_com)

                if len(porcent) > 0:
                    vPorcentajeComision = porcent

                if len(emp) == 0:
                    mensaje = 'Seleccione un empleado.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(emp) > 0:
                        oEmp = Employee.objects.get(pk=emp)
                    elif int(emp) == 0:
                        mensaje = 'Seleccione un empleado.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)
                    else:
                        mensaje = 'Empleado no existe.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = Vendedor.objects.get(pk=id)
                if oMd:
                    oMd.nombre = nombre
                    oMd.grupo_com = oGrpCom
                    oMd.porcentaje_comision = vPorcentajeComision
                    oMd.empleado = oEmp
                    oMd.grupo_comision = oGrpCom
                    oMd.telefono = tel
                    oMd.tel_movil = movil
                    oMd.correo = correo
                    oMd.comentario = coment
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_vendedor(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = Vendedor.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_feriado(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                fecha = request.POST['fecha']
                rate = request.POST['rate']
                comentario = request.POST['comentario']
                activo = int(request.POST['activo'])

                if len(fecha) == 0:
                    mensaje = "El campo 'Fecha' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(rate) == 0:
                    mensaje = "El campo 'Grupo de Comisión' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = Feriado(
                    fecha=fecha,
                    rate=rate,
                    empresa_reg = suc.empresa,
                    descripcion=comentario,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_feriado(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                fecha = request.POST['fecha']
                rate = request.POST['rate']
                comentario = request.POST['comentario']
                activo = int(request.POST['activo'])

                if len(fecha) == 0:
                    mensaje = "El campo 'Fecha' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(rate) == 0:
                    mensaje = "El campo 'Rate' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(comentario) == 0:
                    mensaje = "El campo 'Comentario' es obligatorio."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
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
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_feriado(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = Feriado.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_activo_asignado(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = ActivoAsignado(
                    descripcion=desc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_activo_asignado(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
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
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_activo_asignado(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = ActivoAsignado.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_tipo_salario(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                nombre = request.POST['nombre']
                desc = request.POST['desc']
                dias = request.POST['dias']
                activo = int(request.POST['activo'])

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(nombre) > 5:
                    mensaje = "El campo 'Código' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if validarEntero(dias) != True:
                    mensaje = "El campo 'Días de salario' es de tipo numérico."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = SalaryUnit(
                    code = nombre,
                    description=desc,
                    empresa_reg = suc.empresa,
                    dias_salario = dias,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_tipo_salario(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                desc = request.POST['desc']
                nombre = request.POST['nombre']
                dias = request.POST['dias']
                activo = int(request.POST['activo'])

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if validarEntero(dias) != True:
                    mensaje = "El campo 'Dias de salario' es de tipo numérico."
                    data = {'error': True, 'mensaje': mensaje}
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
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_tipo_salario(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = SalaryUnit.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_costo_empleado(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                nombre = request.POST['nombre']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(nombre) > 5:
                    mensaje = "El campo 'Código' tiene un máximo de 5 carateres."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                suc = Branch.objects.get(pk=request.session["sucursal"])

                oMd = CostUnit(
                    code=nombre,
                    description=desc,
                    empresa_reg = suc.empresa,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_costo_empleado(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                desc = request.POST['desc']
                nombre = request.POST['nombre']
                activo = int(request.POST['activo'])

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = CostUnit.objects.get(pk=id)
                if oMd:
                    oMd.description = desc
                    oMd.name = nombre
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_costo_empleado(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = CostUnit.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_banco(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                nombre = request.POST['nombre']
                desc = request.POST['desc']
                code = request.POST['code']
                activo = int(request.POST['activo'])

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(nombre) > 5:
                    mensaje = "El campo 'Código' tiene como máximo 5 caracteres."
                    data = {'error': True, 'mensaje': mensaje}
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
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_banco(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                desc = request.POST['desc']
                nombre = request.POST['nombre']
                activo = int(request.POST['activo'])

                if len(nombre) == 0:
                    mensaje = "El campo 'Nombre' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = Bank.objects.get(pk=id)
                if oMd:
                    oMd.description = desc
                    oMd.code = nombre
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_banco(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = Bank.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def guardar_empresa_usuario(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                empresa = request.POST['empresa']
                usuario = request.POST['usuario']
                activo = int(request.POST['activo'])
                
                if len(empresa) == 0:
                    mensaje = 'Seleccione una empresa.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(empresa) > 0:
                        oEmpresa = Empresa.objects.get(pk=empresa)
                    elif int(empresa) == 0:
                        mensaje = 'Seleccione una empresa.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)
                    else:
                        mensaje = 'Empleado no existe.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                if len(usuario) == 0:
                    mensaje = 'Seleccione un usuario.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(usuario) > 0:
                        oUsuario = User.objects.get(pk=usuario)
                    elif int(usuario) == 0:
                        mensaje = 'Seleccione un usuario.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)
                    else:
                        mensaje = 'Empleado no existe.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                cReg = UsuarioEmpresa.objects.filter(empresa=oEmpresa, usuario=oUsuario).count()

                if cReg > 0:
                    mensaje = 'La empresa ya está asociada al usuario'
                    data = {
                        'mensaje':mensaje, 'error':True
                    }
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
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def actualizar_empresa_usuario(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                empresa = request.POST['empresa']
                usuario = request.POST['usuario']
                activo = int(request.POST['activo'])

                if len(empresa) == 0:
                    mensaje = 'Seleccione una empresa.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(empresa) > 0:
                        oEmpresa = Empresa.objects.get(pk=empresa)
                    elif int(empresa) == 0:
                        mensaje = 'Seleccione una empresa.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)
                    else:
                        mensaje = 'Empleado no existe.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                if len(usuario) == 0:
                    mensaje = 'Seleccione un usuario.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)
                else:
                    if int(usuario) > 0:
                        oUsuario = User.objects.get(pk=usuario)
                    elif int(usuario) == 0:
                        mensaje = 'Seleccione un usuario.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)
                    else:
                        mensaje = 'Usuario no existe.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                        return JsonResponse(data)

                cReg = UsuarioEmpresa.objects.filter(empresa=oEmpresa, usuario=oUsuario).exclude(pk=id)
                
                if cReg.count() > 0:
                    mensaje = 'La empresa ya está asociada al usuario'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
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
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def eliminar_empresa_usuario(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = UsuarioEmpresa.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def lista_sucursal(request):
    sucursales = None
    idEmpresa = request.GET.get("idEmpresa")
    sucursales_flat =  UsuarioSucursal.objects.filter(usuario=request.user, sucursal__empresa__id=idEmpresa).values_list('sucursal__id', flat=True)
    sucursales = Branch.objects.filter(pk__in=sucursales_flat)
    data = {
        'pk': idEmpresa
    } 
    #return JsonResponse(data)    
    return render(request, 'ajax/lista_sucursales.html', {'sucursales': sucursales})

def lista_estados(request):
    estados = None
    idPais = request.GET.get('idPais')
    estados = State.objects.filter(pais__id=idPais, active=True)
    return render(request, 'ajax/lista_estados.html.', {'estados':estados})

def guardar_foto_perfil(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                empleado_id = request.POST["empleado"]
                tot_reg = ImagenEmpleado.objects.filter(empleado__id=empleado_id).count()
                if tot_reg > 0:
                    instancia = ImagenEmpleado.objects.get(empleado__id=empleado_id)
                    form = ImagenEmpleadoForm(request.POST, request.FILES, instance=instancia)
                    # data = serializers.serialize("json", [instancia,])
                    # data = data.strip("[]")
                    # print data["fields"]
                else:
                    form = ImagenEmpleadoForm(request.POST, request.FILES)
                
                if form.is_valid():
                    print "Entra tambien aqui"
                    form.save()
                    instancia = ImagenEmpleado.objects.get(empleado__id=empleado_id)
                    return render(request, 'ajax/imagen-perfil.html', {'imagen':instancia})
                    #return JsonResponse({'error': False, 'mensaje': 'Se han cargado los datos'})
                else:
                    return JsonResponse({'error': True, 'errors': form.errors})
            else:
                #form = ImagenEmpleadoForm()
                return JsonResponse({'error': True, 'mensaje': 'El método no esta permitido'})
        else:
            return JsonResponse({'error': True, 'mensaje': 'El método no es asíncrono'})
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': ex.message,
        }
        return JsonResponse(data)
    
def enviar_sucursal(request):
    try:
        if request.is_ajax():
            print "Entro a enviar_sucursal"
            IdSucursal = request.GET.get("idSucursal")
            totreg = Branch.objects.filter(pk=IdSucursal).count()
            if totreg > 0:
                sucursal = Branch.objects.get(pk=IdSucursal)
                request.session["nombre_sucursal"] = sucursal.description
                request.session["sucursal"] = IdSucursal
                return JsonResponse({'error': False, 'mensaje': 'Sucursal válida'})
            else:
                request.session["sucursal"] = 0
                request.session["nombre_sucursal"] = ""
                return JsonResponse({'error': True, 'mensaje': 'El método no es asíncrono'})
        else:
            return JsonResponse({'error': True, 'mensaje': 'El método no es asíncrono'})
    except Exception as ex:
        data = {
            'error': True,
            'mensaje': ex.message,
        }
        return JsonResponse(data)

def obtener_ultimo_salario(request):
    try:
        if request.is_ajax():
            IdEmpleado = request.GET.get("idEmpleado")
            aumentos = IncrementosSalariales.objects.filter(empleado__pk=IdEmpleado).order_by('-fecha_incremento')
            if aumentos.count() > 0:
                o_aumento = aumentos[0]
                return JsonResponse({'error': False, 'mensaje': 'Respuesta exitosa', 'salario_anterior':o_aumento.nuevo_salario})
            else:
                return JsonResponse({'error': False, 'mensaje': 'Respuesta exitosa', 'salario_anterior': 0.00})
        else:
            return JsonResponse({'error': True, 'mensaje': 'El método no es asíncrono'})
    except Exception as ex:
        data = {
            'error': True,
            'mensaje': ex.message,
        }
        return JsonResponse(data)

#region Codigo para Aumento de Sueldo
@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.see_incrementossalariales', raise_exception=True)
def aumento_salario_listado(request):
    lista = []
    busqueda = None
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(empresa_reg=suc.empresa)
    if 'empleado' in request.GET:
        emp = request.GET.get("empleado")
        if len(emp) > 0:
            if int(emp) > 0:
                busqueda = int(emp)
                empleado = Employee.objects.get(pk=busqueda)
                print empleado
                lista = IncrementosSalariales.objects.filter(empleado=empleado, empresa_reg = suc.empresa)
                print lista
            else:
                lista = IncrementosSalariales.objects.filter(empresa_reg = suc.empresa)
    else:
        lista = IncrementosSalariales.objects.filter(empresa_reg = suc.empresa)

    # suc = Branch.objects.get(pk=request.session["sucursal"])
    # empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, 'aumento-salario-listado.html', {'empleados': empleados, 'datos':lista, 'busqueda': busqueda})

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.add_incrementossalariales', raise_exception=True)
def aumento_salario_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    motivos = MotivoAumentoSueldo.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, 'aumento-salario-form.html', {'empleados': empleados, 'motivos':motivos})

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.change_incrementossalariales', raise_exception=True)
def aumento_salario_editar(request, id):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    empleados = Employee.objects.filter(active=True, empresa_reg=suc.empresa)
    motivos = MotivoAumentoSueldo.objects.filter(active=True, empresa_reg=suc.empresa)
    dato = IncrementosSalariales.objects.get(pk=id)
    dato = {
        'pk': dato.pk,
        'empleado': dato.empleado,
        'fecha_incremento': dato.fecha_incremento,
        'motivo_aumento':dato.motivo_aumento,
        'salario_anterior': locale.format("%.2f", dato.salario_anterior, grouping=True),
        'incremento': locale.format("%.2f", dato.incremento, grouping=True),
        'nuevo_salario': locale.format("%.2f", dato.nuevo_salario, grouping=True),
        'comentarios': dato.comentarios
    }
    return render(request, 'aumento-salario-form.html', {'empleados': empleados, 'dato': dato, 'motivos':motivos , 'editar':True})

#------------------ AJAX -----------------------
def aumento_salario_guardar(request):
    fecha_incremento = ""
    salario_anterior = 0.00
    incremento = 0.00
    nuevo_salario = 0.00
    try:
        if request.is_ajax():
            if request.method == 'POST':
                empleado_fk = request.POST['empleado_fk']
                fecha_incremento = request.POST['fecha_incremento']
                motivo_aumento_fk = request.POST['motivo_aumento']
                salario_anterior = request.POST['salario_anterior']
                incremento = request.POST['incremento']
                nuevo_salario = request.POST['nuevo_salario']
                comentarios = request.POST['comentarios']
                if int(empleado_fk) == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "empleado" es obligatorio.'})
                else:
                    empleados = Employee.objects.filter(pk=empleado_fk)
                    if empleados.count() > 0:
                        o_empleado = Employee.objects.get(pk=empleado_fk)
                    else:
                        return JsonResponse({'error': True, 'mensaje': 'El empleado no existe.'})

                if len(fecha_incremento) == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "Fecha de Incremento" es obligatorio.'})

                if motivo_aumento_fk == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "motivo de aumento" es obligatorio.'})
                else:
                    motivos = MotivoAumentoSueldo.objects.filter(pk=motivo_aumento_fk)
                    if motivos.count() > 0:
                        o_motivo = MotivoAumentoSueldo.objects.get(pk=motivo_aumento_fk)
                    else:
                        return JsonResponse({'error': True, 'mensaje': 'El "motivo de aumento" no existe.'})

                aumentos = IncrementosSalariales.objects.filter(empleado=o_empleado, fecha_incremento=fecha_incremento)

                if aumentos.count() > 0:
                    return JsonResponse({'error': True, 'mensaje': 'Ya existe un registro de aumento para el empleado en la fecha seleccionada.'})

                if validarDecimal(incremento) == False:
                    return JsonResponse({'error': True, 'mensaje': 'El tipo de dato no es válido.'})
                else:
                    if incremento == 0:
                        return JsonResponse({'error': True, 'mensaje': 'El incremento tiene que ser mayor a cero.'})

                suc = Branch.objects.get(pk=request.session["sucursal"])
                oIncremento = IncrementosSalariales(
                    empleado = o_empleado,
                    fecha_incremento = fecha_incremento,
                    motivo_aumento = o_motivo,
                    salario_anterior = salario_anterior,
                    incremento = incremento,
                    nuevo_salario = nuevo_salario,
                    comentarios = comentarios,
                    salario_actual = True,
                    empresa_reg = suc.empresa,
                    user_reg = request.user,
                    active=True
                )
                oIncremento.save()
                return JsonResponse({'error': False, 'mensaje': 'Se ha guardado el registro de Aumento de salario.'})
            else:
                return JsonResponse({'error': True, 'mensaje': 'El método no está permitido.'})
        else:
            pass
        return JsonResponse({'error': False, 'mensaje': 'Respuesta exitosa'})
    except Exception as ex:
        data = {
            'error': True,
            'mensaje': ex.message,
        }
        return JsonResponse(data)

def aumento_salario_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = request.POST["id"]
                motivo = request.POST["motivo"]
                fecha_incremento = request.POST["fecha_incremento"]
                incremento = request.POST["incremento"]
                nuevo_salario = request.POST["incremento"]

                if motivo == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "motivo de aumento" es obligatorio.'})
                else:
                    motivos = MotivoAumentoSueldo.objects.filter(pk=motivo)
                    if motivos.count() > 0:
                        o_motivo = MotivoAumentoSueldo.objects.get(pk=motivo)
                    else:
                        return JsonResponse({'error': True, 'mensaje': 'El "motivo de aumento" no existe.'})

                if validarDecimal(incremento) == False:
                    return JsonResponse({'error': True, 'mensaje': 'El tipo de dato no es válido.'})
                else:
                    if incremento == 0:
                        return JsonResponse({'error': True, 'mensaje': 'El incremento tiene que ser mayor a cero.'})

                tot_reg = IncrementosSalariales.objects.filter(pk=id).count()
                if tot_reg > 0:
                    o_Incremento = IncrementosSalariales.objects.get(pk=id)
                    o_Incremento.motivo_aumento = o_motivo
                    o_Incremento.fecha_incremento = fecha_incremento
                    o_Incremento.incremento = incremento
                    o_Incremento.nuevo_salario = nuevo_salario
                    o_Incremento.save()
                    return JsonResponse({'error': False, 'mensaje': 'Se ha guardado el registro.'})
                else:
                    return JsonResponse({'error': True, 'mensaje': 'El registro no existe.'})
            else:
                return JsonResponse({'error': True, 'mensaje': 'El método no está permitido.'})
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
            return JsonResponse(data)
    except Exception as ex:
        data = {
            'error': True,
            'mensaje': ex.message,
        }
        return JsonResponse(data)

def aumento_salario_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = IncrementosSalariales.objects.get(pk=reg_id)
                    empleado_id = oMd.empleado.pk
                    if oMd:
                        oMd.delete()
                        regs = IncrementosSalariales.objects.filter(empleado__pk=empleado_id).order_by('-fecha_incremento')[:1]
                        if regs.count() > 0:
                            incremento = regs[0]
                            incremento.salario_actual = True
                            incremento.save()
                            regs = Employee.objects.filter(pk=empleado_id)
                            if regs.count() > 0:
                                empleado = Employee.objects.get(pk=empleado_id)
                                empleado.salary = incremento.nuevo_salario
                                if empleado.salaryUnits:
                                    tot_reg = SalaryUnit.objects.filter(pk=empleado.salaryUnits.pk).count()
                                    if tot_reg > 0:
                                        o_salary_units = SalaryUnit.objects.get(pk=empleado.salaryUnits.pk)
                                        if o_salary_units.dias_salario > 0:
                                            empleado.salario_diario = float(incremento.nuevo_salario) / float(o_salary_units.dias_salario)
                                empleado.save()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def aumento_salario_ver_registro(request):
    error = False
    mensaje = ""
    titulo = ""
    dato = None
    id = 0
    if request.is_ajax():
        id = request.GET.get('id')
        if id == 0:
            error = True
            mensaje = "El registro no existe."
        else:
            tot_reg = IncrementosSalariales.objects.filter(pk=id).count()
            if tot_reg > 0:
                dato = IncrementosSalariales.objects.get(pk=id)
                dato = {
                    'pk': dato.pk,
                    'empleado': dato.empleado,
                    'fecha_incremento': dato.fecha_incremento,
                    'motivo_aumento': dato.motivo_aumento,
                    'salario_anterior': locale.format("%.2f", dato.salario_anterior, grouping=True),
                    'incremento': locale.format("%.2f", dato.incremento, grouping=True),
                    'nuevo_salario': locale.format("%.2f", dato.nuevo_salario, grouping=True),
                    'comentarios': dato.comentarios
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
    return render(request, 'ajax/aumento-salario-modal.html', {'error':error, 'mensaje': mensaje, 'titulo':titulo, 'dato':dato})


#----------------- END AJAX --------------------


#endregion

#region Código para Empleado

#---------------------------AJAX-----------------------------

def obtener_dias_salario(request):
    try:
        if request.is_ajax():
            Id = request.GET.get("id")
            tot_reg = SalaryUnit.objects.filter(pk=Id)
            if tot_reg.count() > 0:
                tipo_salario = SalaryUnit.objects.get(pk=Id)
                return JsonResponse({'error': False, 'mensaje': 'Respuesta exitosa', 'dias_salario':tipo_salario.dias_salario})
            else:
                return JsonResponse({'error': True, 'mensaje': 'El tipo de salario no existe.'})
        else:
            return JsonResponse({'error': True, 'mensaje': 'El método no es asíncrono'})
    except Exception as ex:
        data = {
            'error': True,
            'mensaje': ex.message,
        }
        return JsonResponse(data) 

#--------------------------END AJAX -------------------------

#endregion

#region Código para Ingreso Individual

def ingreso_individual_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_ingresoindividual"):
        lista = IngresoIndividual.objects.filter(empresa_reg=suc.empresa)
    else:
        lista = IngresoIndividual.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(request, 'ingreso-individual-listado.html', {'lista':lista})

def ingreso_individual_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    tipos_ingresos = TipoIngreso.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(request, 'ingreso-individual-form.html', {'tipos_ingresos':tipos_ingresos})

#---------------------AJAX-------------------------------

def ingreso_individual_guardar(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                ingreso_i = request.POST['ingreso_i']
                tipo_ingreso = request.POST['tipo_ingreso']
                activo = int(request.POST['activo'])

                if len(ingreso_i) == 0:
                    mensaje = "El campo 'Ingreso Individual' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(tipo_ingreso) == 0:
                    mensaje = "El campo 'Tipo Ingreso' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if tipo_ingreso == 0:
                    mensaje = "El campo 'Tipo Ingreso' tiene como máximo 100 caracteres."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(tipo_nomina) > 50:
                    mensaje = "El campo 'Ingrseo individual' tiene como máximo 100 caracteres."
                    data = {'error': True, 'mensaje': mensaje}
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
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)


#---------------------AJAX-------------------------------

#endregion

#region Código para Planilla


@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.see_planilla', raise_exception=True)
def planilla_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_planilla"):
        datos = Planilla.objects.filter(empresa_reg=suc.empresa, active=True)
    else:
        datos = Planilla.objects.filter(sucursal_reg=suc, active=True)
    return render(request, 'planilla-listado.html', {'datos':datos})


@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.add_planilla', raise_exception=True)
def planilla_form(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    tipo_pago = SalaryUnit.objects.filter(empresa_reg=suc.empresa, active=True)
    tipo_planilla = TipoNomina.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(request, 'planilla-form.html',{'tipo_planilla':tipo_planilla, 'tipos_pago':tipo_pago})

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.change_planilla', raise_exception=True)
def planilla_editar(request, id):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    tipo_pago = SalaryUnit.objects.filter(empresa_reg=suc.empresa, active=True)
    tipo_planilla = TipoNomina.objects.filter(empresa_reg=suc.empresa, active=True)
    o_planilla = Planilla.objects.get(pk=id)
    return render(request, 'planilla-form.html',{'editar':True,'tipo_planilla':tipo_planilla, 'tipos_pago':tipo_pago, 'dato':o_planilla})

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.play_planilla', raise_exception=True)
def planilla_generar(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_planilla"):
        planillas = Planilla.objects.filter(empresa_reg=suc.empresa, active=True, cerrada=False)
    else:
        planillas = Planilla.objects.filter(sucursal_reg=suc, active=True, cerrada=False)
    return render(request, 'planilla-generar.html', {'planillas':planillas})

#--------------------------------AJAX-----------------------------------

def obtener_empleados_planilla(request):
    try:
        mensaje = ''
        codigos =  {}
        l_empleados = []
        if request.is_ajax():
            id = request.GET.get('id')
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
                    empleados = Employee.objects.filter(active=True, tipo_nomina=o_planilla.tipo_planilla, salaryUnits=o_planilla.frecuencia_pago, branch=suc)
                    if empleados.count() > 0:
                        for item in empleados:
                            codigo = {'ID': item.pk}
                            l_empleados.append(codigo)
                        error = False
                        data = {'error':error, 'empleados':l_empleados}
                        return JsonResponse(data)
                    else:
                        data = {'error':True, 'mensaje':"No encontraron empleados pertenecientes a la planilla."}
                        return JsonResponse(data)
                else:
                    error = True
                    mensaje = "No existe el registro."
        else:
            error = True
            mensaje = "El método no está permitido."
        data = {'error': error, 'mensaje':mensaje}
        return JsonResponse(data)
    except Exception as ex:
        data = {
            'error': True,
            'mensaje': ex.message,
        }
        return JsonResponse(data)

def planilla_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = request.POST["id"]
                tipo_planilla_id = request.POST['tipo_planilla']
                tipo_pago_id = request.POST['tipo_pago']
                fecha_pago = request.POST['fecha_pago']
                fecha_inicio = request.POST['fecha_inicio']
                fecha_fin = request.POST['fecha_fin']
                descripcion = request.POST['descripcion']

                if int(tipo_planilla_id) == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "Tipo de Planilla" es obligatorio.'})
                else:
                    tipos_planilla = TipoNomina.objects.filter(
                        pk=tipo_planilla_id)
                    if tipos_planilla.count() > 0:
                        o_tipo_planilla = TipoNomina.objects.get(
                            pk=tipo_planilla_id)
                    else:
                        return JsonResponse({'error': True, 'mensaje': 'El Tipo de Planilla no existe.'})

                if int(tipo_pago_id) == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "Tipo de Pago" es obligatorio.'})
                else:
                    tipos_pago = SalaryUnit.objects.filter(pk=tipo_pago_id)
                    if tipos_pago.count() > 0:
                        o_tipo_pago = SalaryUnit.objects.get(pk=tipo_pago_id)
                    else:
                        return JsonResponse({'error': True, 'mensaje': 'El Tipo de Pago no existe.'})

                if len(fecha_pago) == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "Fecha de Pago" es obligatorio.'})

                if len(fecha_inicio) == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "Fecha de Inicio" es obligatorio.'})

                if len(fecha_fin) == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "Fecha de Fin" es obligatorio.'})

                if len(descripcion) == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "Descripcion" es obligatorio.'})

                tot_reg = Planilla.objects.filter(pk=id).count()
                if tot_reg > 0:
                    o_Mdl = Planilla.objects.get(pk=id)
                    if o_Mdl.cerrada:
                        return JsonResponse({'error': True, 'mensaje': 'La planilla ya está cerrada.'})
                    o_Mdl.tipo_planilla = o_tipo_planilla
                    o_Mdl.frecuencia_pago = o_tipo_pago
                    o_Mdl.fecha_pago = fecha_pago
                    o_Mdl.fecha_inicio = fecha_inicio
                    o_Mdl.fecha_fin = fecha_fin
                    o_Mdl.descripcion = descripcion
                    o_Mdl.save()
                    return JsonResponse({'error': False, 'mensaje': 'Se ha guardado el registro.'})
                else:
                    return JsonResponse({'error': True, 'mensaje': 'El registro no existe.'})
            else:
                return JsonResponse({'error': True, 'mensaje': 'El método no está permitido.'})
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
            return JsonResponse(data)
    except Exception as ex:
        data = {
            'error': True,
            'mensaje': ex.message,
        }
        return JsonResponse(data)

def planilla_guardar(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                tipo_planilla_id = request.POST['tipo_planilla']
                tipo_pago_id = request.POST['tipo_pago']
                fecha_pago = request.POST['fecha_pago']
                fecha_inicio = request.POST['fecha_inicio']
                fecha_fin = request.POST['fecha_fin']
                descripcion = request.POST['descripcion']
                
                if int(tipo_planilla_id) == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "Tipo de Planilla" es obligatorio.'})
                else:
                    tipos_planilla = TipoNomina.objects.filter(pk=tipo_planilla_id)
                    if tipos_planilla.count() > 0:
                        o_tipo_planilla = TipoNomina.objects.get(pk=tipo_planilla_id)
                    else:
                        return JsonResponse({'error': True, 'mensaje': 'El Tipo de Planilla no existe.'})

                if int(tipo_pago_id) == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "Tipo de Pago" es obligatorio.'})
                else:
                    tipos_pago = SalaryUnit.objects.filter(pk=tipo_pago_id)
                    if tipos_pago.count() > 0:
                        o_tipo_pago = SalaryUnit.objects.get(pk=tipo_pago_id)
                    else:
                        return JsonResponse({'error': True, 'mensaje': 'El Tipo de Pago no existe.'})

                if len(fecha_pago) == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "Fecha de Pago" es obligatorio.'})
                
                if len(fecha_inicio) == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "Fecha de Inicio" es obligatorio.'})

                if len(fecha_fin) == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "Fecha de Fin" es obligatorio.'})

                if len(descripcion) == 0:
                    return JsonResponse({'error': True, 'mensaje': 'El campo "Descripcion" es obligatorio.'})

                suc = Branch.objects.get(pk=request.session["sucursal"])
                oPlanilla = Planilla(
                    correlativo = 1,
                    tipo_planilla = o_tipo_planilla,
                    descripcion = descripcion,
                    frecuencia_pago = o_tipo_pago,
                    fecha_inicio = fecha_inicio,
                    fecha_fin = fecha_fin,
                    fecha_pago = fecha_pago,
                    cerrada = False,
                    empresa_reg = suc.empresa,
                    sucursal_reg = suc,
                    active=True,
                    user_reg = request.user
                )
                
                oPlanilla.save()
                return JsonResponse({'error': False, 'mensaje': 'Se ha guardado el registro de Planilla.'})
            else:
                return JsonResponse({'error': True, 'mensaje': 'El método no está permitido.'})
        else:
            pass
        return JsonResponse({'error': False, 'mensaje': 'Respuesta exitosa'})
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': ex.message,
        }
        return JsonResponse(data)

import time
def planilla_calculos_empleado(request):
    data = {}
    try:
        if request.is_ajax():
            if request.method == 'POST':
                total_dias = 0
                dias_ausencia_con_pago = 0
                dias_ausencia_sin_pago = 0
                empleado_id = request.POST["empleado_id"]
                planilla_id = request.POST["planilla_id"]
                o_empleado = Employee.objects.get(pk=empleado_id)
                o_planilla = Planilla.objects.get(pk=planilla_id)
                suc = Branch.objects.get(pk=request.session["sucursal"])
                ausencias_con_pago = Ausentismo.objects.filter(empleado=o_empleado, sucursal_reg=suc, motivo__pagado=True, desde__gte=o_planilla.fecha_inicio, desde__lte=o_planilla.fecha_fin, hasta__gte=o_planilla.fecha_inicio, hasta__lte=o_planilla.fecha_fin)
                if ausencias_con_pago.count() > 0:
                    dias_ausencia_con_pago = 1
                    for item in ausencias_con_pago:
                        dias_ausencia_con_pago = dias_ausencia_con_pago + (item.hasta - item.desde).days

                ausencias_sin_pago = Ausentismo.objects.filter(empleado=o_empleado, sucursal_reg=suc, motivo__pagado=False, desde__gte=o_planilla.fecha_inicio, desde__lte=o_planilla.fecha_fin, hasta__gte=o_planilla.fecha_inicio, hasta__lte=o_planilla.fecha_fin)
                if ausencias_sin_pago.count() > 0:
                    dias_ausencia_sin_pago = 1
                    for item in ausencias_sin_pago:
                        dias_ausencia_sin_pago = dias_ausencia_sin_pago + (item.hasta - item.desde).days
                o_planilladetalle = PlanillaDetalle(
                    planilla = o_planilla,
                    empleado = o_empleado,
                    salario_diario = o_empleado.salario_diario,
                    dias_salario = o_planilla.frecuencia_pago.dias_salario,
                    dias_ausentes_sin_pago = dias_ausencia_sin_pago,
                    dias_ausentes_con_pago = dias_ausencia_con_pago,
                    empresa_reg = suc.empresa,
                    sucursal_reg = suc,
                    active = True,
                    user_reg = request.user
                )
                o_planilladetalle.save()
                data = {
                    'error': False,
                    'mensaje': "El proceso ha finalizado.",
                }
            else:
                data = {
                    'error': True,
                    'mensaje': "El método no está permitido.",
                }
        else:
            data = {
                'error': True,
                'mensaje': "La solicitud no es asíncrona.",
            }
    except Exception as ex:
        data = {
            'error': True,
            'mensaje': ex.message,
        }
    return JsonResponse(data)

def planilla_ver_registro(request):
    error = False
    mensaje = ""
    titulo = ""
    dato = None
    id = 0
    if request.is_ajax():
        id = request.GET.get('id')
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
    return render(request, 'ajax/planilla-modal.html', {'error':error, 'mensaje': mensaje, 'titulo':titulo, 'dato':dato})

#------------------------------END AJAX---------------------------------

#endregion

#region Código para Tipo de Nomina
@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.see_tiponomina', raise_exception=True)
def tipo_nomina_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    listado = TipoNomina.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, 'tipo-nomina-listado.html', {'listado':listado})

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.add_tiponomina', raise_exception=True)
def tipo_nomina_form(request):
    return render(request, 'tipo-nomina-form.html')

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.change_tiponomina', raise_exception=True)
def tipo_nomina_editar(request, id):
    dato = TipoNomina.objects.get(pk=id)
    return render(request, 'tipo-nomina-form.html', {'dato':dato, 'editar':True})

#---------------------AJAX-------------------------------

def tipo_nomina_guardar(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                tipo_nomina = request.POST['tipo_nomina']
                desc = request.POST['descripcion']
                activo = int(request.POST['activo'])

                if len(tipo_nomina) == 0:
                    mensaje = "El campo 'Tipo Nómina' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(tipo_nomina) > 100:
                    mensaje = "El campo 'Tipo Nómina' tiene como máximo 100 caracteres."
                    data = {'error': True, 'mensaje': mensaje}
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
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def tipo_nomina_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                tipo_nomina = request.POST['tipo_nomina']
                desc = request.POST['descripcion']
                activo = int(request.POST['activo'])

                if len(tipo_nomina) == 0:
                    mensaje = "El campo 'Tipo Nómina' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(tipo_nomina) > 100:
                    mensaje = "El campo 'Tipo Nómina' tiene como máximo 100 caracteres."
                    data = {'error': True, 'mensaje': mensaje}
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
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def tipo_nomina_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = TipoNomina.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

#---------------------END AJAX---------------------------

# endregion 

#region Código para Tipo de Ingreso

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.see_tipoingreso', raise_exception=True)
def tipo_ingreso_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    lista = TipoIngreso.objects.filter(empresa_reg=suc.empresa, active=True)
    return render(request, 'tipo-ingreso-listado.html', {'lista':lista})

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.add_tipoingreso', raise_exception=True)
def tipo_ingreso_form(request):
    return render(request, 'tipo-ingreso-form.html')


@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.change_tipoingreso', raise_exception=True)
def tipo_ingreso_editar(request, id):
    dato = TipoIngreso.objects.get(pk=id)
    return render(request, 'tipo-ingreso-form.html', {'dato': dato, 'editar': True})

#---------------------AJAX-------------------------------


def tipo_ingreso_guardar(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                tipo_ingreso = request.POST['tipo_ingreso']
                desc = request.POST['descripcion']
                activo = int(request.POST['activo'])

                if len(tipo_ingreso) == 0:
                    mensaje = "El campo 'Tipo Ingreso' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(tipo_ingreso) > 100:
                    mensaje = "El campo 'Tipo Ingreso' tiene como máximo 100 caracteres."
                    data = {'error': True, 'mensaje': mensaje}
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
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def tipo_ingreso_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                tipo_ingreso = request.POST['tipo_ingreso']
                desc = request.POST['descripcion']
                activo = int(request.POST['activo'])

                if len(tipo_ingreso) == 0:
                    mensaje = "El campo 'Tipo Ingreso' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(tipo_ingreso) > 100:
                    mensaje = "El campo 'Tipo Ingreso' tiene como máximo 100 caracteres."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if activo == 1:
                    activo = True
                else:
                    activo = False

                oMd = TipoIngreso.objects.get(pk=id)
                if oMd:
                    oMd.tipo_ingreso = tipo_ingreso
                    oMd.descripcion = desc
                    oMd.active = activo
                    oMd.user_mod = request.user
                    oMd.date_mod = datetime.datetime.now()
                    oMd.save()
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def tipo_ingreso_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = TipoIngreso.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

#---------------------AJAX-------------------------------

#endregion

#region Código para Tipo de Contrato

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.see_tipocontrato', raise_exception=True)
def tipo_contrato_listado(request):
    suc = Branch.objects.get(pk=request.session["sucursal"])
    if request.user.has_perm("worksheet.see_all_tipocontrato"):
        listado = TipoContrato.objects.filter(empresa_reg=suc.empresa)
    else:
        listado = TipoContrato.objects.filter(active=True, empresa_reg=suc.empresa)
    return render(request, 'tipo-contrato-listado.html', {'listado':listado})

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.add_tipocontrato', raise_exception=True)
def tipo_contrato_form(request):
    return render(request, 'tipo-contrato-form.html')

@login_required(login_url='/form/iniciar-sesion/')
@permission_required('worksheet.change_tipocontrato', raise_exception=True)
def tipo_contrato_editar(request, id):
    dato = TipoContrato.objects.get(pk=id)
    return render(request, 'tipo-contrato-form.html', {'editar':True, 'dato':dato})

#---------------------AJAX-------------------------------

def tipo_contrato_guardar(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                tipo_contrato = request.POST['tipo_contrato']
                desc = request.POST['descripcion']
                activo = int(request.POST['activo'])

                if len(tipo_contrato) == 0:
                    mensaje = "El campo 'Tipo de Contrato' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(tipo_contrato) > 100:
                    mensaje = "El campo 'Tipo Contrato' tiene como máximo 100 caracteres."
                    data = {'error': True, 'mensaje': mensaje}
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
                mensaje = 'Se ha guardado el registro'
                data = {
                    'mensaje': mensaje, 'error': False
                }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def tipo_contrato_actualizar(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                id = int(request.POST['id'])
                tipo_contrato = request.POST['tipo_contrato']
                desc = request.POST['descripcion']
                activo = int(request.POST['activo'])

                if len(tipo_contrato) == 0:
                    mensaje = "El campo 'Tipo Nómina' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(desc) == 0:
                    mensaje = "El campo 'Descripción' es obligatorio."
                    data = {'error': True, 'mensaje': mensaje}
                    return JsonResponse(data)

                if len(tipo_contrato) > 100:
                    mensaje = "El campo 'Tipo Nómina' tiene como máximo 100 caracteres."
                    data = {'error': True, 'mensaje': mensaje}
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
                    mensaje = 'Se ha actualizado el registro.'
                    data = {
                        'mensaje': mensaje, 'error': False
                    }
                else:
                    mensaje = "No existe el registro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "No es una petición AJAX."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

def tipo_contrato_eliminar(request):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                reg_id = request.POST['id']
                if int(reg_id) > 0:
                    oMd = TipoContrato.objects.get(pk=reg_id)
                    if oMd:
                        oMd.delete()
                        mensaje = 'Se ha eliminado el registro.'
                        data = {
                            'mensaje': mensaje, 'error': False
                        }
                    else:
                        mensaje = 'No existe el registro.'
                        data = {
                            'mensaje': mensaje, 'error': True
                        }
                else:
                    mensaje = "No se pasó ningún parámetro."
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
            else:
                mensaje = "Método no permitido."
                data = {
                    'mensaje': mensaje, 'error': True
                }
        else:
            mensaje = "Tipo de petición no permitido."
            data = {
                'mensaje': mensaje, 'error': True
            }
    except Exception as ex:
        print ex
        data = {
            'error': True,
            'mensaje': 'error',
        }
    return JsonResponse(data)

#---------------------END AJAX---------------------------

#endregion

#--------------------------VALIDACIONES------------------------------
def validarEntero(dato):
    try:
        dato = int(dato)
        dato += 1
        dato = dato / 1
        return True
    except TypeError:
        return False

def validarDecimal(dato):
    try:
        dato = float(dato)
        return True
    except TypeError:
        return False
