# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from worksheet.models import *
import datetime
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
@login_required(login_url='/seguridad/login/')
def home(request):
    empleados = Employee.objects.all()
    return render(request, 'index.html', {'empleados':empleados})

def empleado_form(request):
    positions = Position.objects.filter(active=True)
    departments = Department.objects.filter(active=True)
    branches = Branch.objects.filter(active=True)
    salesPersons = SalesPerson.objects.filter(active=True)
    states = State.objects.filter(active=True)
    countries = Country.objects.filter(active=True)
    estados_emp = StatusEmp.objects.filter(active=True)
    terms = TermReason.objects.filter(active=True)
    sexos = Sex.objects.filter(active=True)
    citizenships = Country.objects.filter(active=True)
    civil_status = CivilStatus.objects.filter(active=True)
    salary_units = SalaryUnit.objects.filter(active=True)
    costs_units = CostUnit.objects.filter(active=True)
    banks = Bank.objects.filter(active=True)
    return render(request, 'empleado-form.html', {'banks':banks, 'costs_units': costs_units, 'salary_units': salary_units, 'civil_status':civil_status, 'citizenships':citizenships, 'positions':positions, 'departments':departments, 'branches':branches, 'salesPersons':salesPersons, 'states':states, 'countries':countries, 'stats':estados_emp, 'terms':terms, 'sexs':sexos})

def empleado_listado(request):
    empleados = Employee.objects.all()
    return render(request, 'empleado-listado.html', {'empleados':empleados})

def empleado_perfil(request):
    return render(request, 'perfil-empleado.html')

def corporativo(request):
    return render(request, 'corporativo.html')

def corporativo_editar(request, reg_id):
    dato = GrupoCorporativo.objects.get(pk=reg_id)
    return render(request, 'corporativo.html', {'dato':dato, 'editar':True})

def listadoCorporativo(request):
    corporativos = GrupoCorporativo.objects.all().order_by('date_reg')
    return render(request, 'corporativo-listado.html', {'corporativos':corporativos})

def empresa(request):
    return render(request, 'empresa.html')

def empresa_editar(request, emp_id):
    dato = Empresa.objects.get(pk=emp_id)
    return render(request, 'empresa.html', {'dato':dato, 'editar':True} )

def listadoEmpresa(request):
    empresas = Empresa.objects.all()
    return render(request, 'empresa-listado.html', {'empresas':empresas})

def sucursal(request):
    return render(request, 'sucursal.html')

def sucursal_editar(request, id):
    dato = Branch.objects.get(pk=id)
    return render(request, 'sucursal.html', {'editar':True, 'dato':dato})

def listadoSucursal(request):
    sucursales = Branch.objects.all()
    return render(request, 'sucursal-listado.html', {'sucursales':sucursales})

def divisiones(request):
    return render(request, 'divisiones.html')

def division_editar(request, id):
    dato = Divisiones.objects.get(pk=id)
    return render(request, 'divisiones.html', {'editar':True, 'dato':dato})

def listadoDivisiones(request):
    divisiones = Divisiones.objects.all()
    return render(request, 'divisiones-listado.html', {'divisiones':divisiones})

def departamentos(request):
    return render(request, 'departamentos.html')

def departamento_editar(request, id):
    dato = Department.objects.get(pk=id)
    return render(request, 'departamentos.html', {'editar':True, 'dato':dato})

def listadoDepartamentos(request):
    deptos = Department.objects.all()
    return render(request, 'departamento-listado.html', {'deptos':deptos})

def puestoTrabajo(request):
    return render(request, 'puesto-trabajo.html')

def puesto_editar(request, id):
    dato = Position.objects.get(pk=id)
    return render(request, 'puesto-trabajo.html', {'editar':True, 'dato':dato})

def listadoPuestoTrabajo(request):
    puestos = Position.objects.all()
    return render(request, 'puestos-listado.html', {'puesto':puestos})

def centro_costos(request):
    return render(request, 'centro-costos.html')

def centro_costo_editar(request, id):
    dato = CentrosCostos.objects.get(pk=id)
    return render(request, 'centro-costos.html', {'editar':True, 'dato':dato})

def listadoCentroCostos(request):
    ccostos = CentrosCostos.objects.all()
    return render(request, 'ccostos-listado.html', {'ccostos':ccostos})

def paises(request):
    return render(request, 'paises.html')

def paises_editar(request, id):
    dato = Country.objects.get(pk=id)
    return render(request, 'paises.html', {'editar':True, 'dato':dato})

def listadoPaises(request):
    paises = Country.objects.all()
    return render(request, 'paises-listado.html', {'paises':paises})

def deptos_pais(request):
    return render(request, 'deptos-pais.html')

def deptos_pais_editar(request, id):
    dato = State.objects.get(pk=id)
    return render(request, 'deptos-pais.html', {'editar':True, 'dato':dato})

def deptos_pais_listado(request):
    deptos = State.objects.all()
    return render(request, 'deptos-pais-listado.html', {'deptos': deptos})

def ciudad(request):
    return render(request, 'ciudad.html')

def ciudad_editar(request, id):
    dato = Ciudad.objects.get(pk=id)
    return render(request, 'ciudad.html', {'editar':True, 'dato':dato})

def ciudades_listado(request):
    ciudades = Ciudad.objects.all()
    return render(request, 'ciudades-listado.html', {'ciudades':ciudades})

def genero(request):
    return render(request, 'genero.html')

def genero_editar(request, id):
    dato = Sex.objects.get(pk=id)
    return render(request, 'genero.html', {'editar':True, 'dato':dato})

def generos_listado(request):
    generos = Sex.objects.all()
    return render(request, 'genero-listado.html', {'generos':generos})

def estado_civil(request):
    return render(request, 'estado-civil.html')

def estado_civil_editar(request, id):
    dato = CivilStatus.objects.get(pk=id)
    return render(request, 'estado-civil.html', {'editar':True, 'dato':dato})

def estado_civil_listado(request):
    estados = CivilStatus.objects.all()
    return render(request, 'estado-civil-listado.html', {'estados':estados})

def parentesco(request):
    return render(request, 'parentesco.html')

def parentesco_editar(request, id):
    dato = Parentesco.objects.get(pk=id)
    return render(request, 'parentesco.html', {'editar':True, 'dato':dato})

def parentesco_listado(request):
    parentescos = Parentesco.objects.all()
    return render(request, 'parentesco-listado.html', {'parentescos':parentescos})

def funcion_trabajo(request):
    return render(request, 'funciones-trabajo.html')

def funcion_trabajo_editar(request, id):
    funcion = FuncionesTrabajo.objects.get(pk=id)
    return render(request, 'funciones-trabajo.html', {'dato':funcion, 'editar':True})

def funcion_trab_listado(request):
    funciones = FuncionesTrabajo.objects.all()
    return render(request, 'funciones-trabajo-listado.html', {'funciones': funciones})

def equipo_trabajo(request):
    return render(request, 'equipo-trabajo.html' )

def equipo_trabajo_editar(request, id):
    dato = EquipoTrabajo.objects.get(pk=id)
    return render(request, 'equipo-trabajo.html', {'editar':True, 'dato':dato})

def equipo_trabajo_listado(request):
    equipos = EquipoTrabajo.objects.all()
    return render(request, 'equipo-trabajo-listado.html', {'equipos':equipos})

def estado_empleado(request):
    return render(request, 'estatus-empleado.html')

def estado_empleado_editar(request, id):
    dato = StatusEmp.objects.get(pk=id)
    return render(request, 'estatus-empleado.html', {'editar':True, 'dato':dato})

def estado_empleado_listado(request):
    lista = StatusEmp.objects.all()
    return render(request, 'estado-empleado-listado.html', {'lista':lista})

def ausentismo(request):
    empleados = Employee.objects.filter(active=True)
    return render(request, 'ausentismo.html', {'empleados':empleados})

def ausentismo_editar(request, id):
    dato = Ausentismo.objects.get(pk=id)
    empleados = Employee.objects.filter(active=True)
    return render(request, 'ausentismo.html', {'editar':True, 'dato':dato, 'empleados':empleados})

def ausentismo_listado(request):
    lista = Ausentismo.objects.all().order_by('-desde')
    return render(request, 'ausentismo-listado.html', {'lista':lista})

def motivos_ausencia(request):
    return render(request, 'motivos-ausencia.html')

def motivos_ausencia_editar(request, id):
    dato = MotivosAusencia.objects.get(pk=id)
    return render(request, 'motivos-ausencia.html', {'editar':True, 'dato':dato})

def motivos_ausencia_listado(request):
    lista = MotivosAusencia.objects.all()
    return render(request, 'motivos-ausencia-listado.html', {'lista':lista})

def motivo_despido(request):
    return render(request, 'motivos-despido.html')

def motivo_despido_editar(request, id):
    dato = MotivosDespido.objects.get(pk=id)
    return render(request, 'motivos-despido.html', {'editar':True, 'dato':dato})

def motivos_despido_listado(request):
    lista = MotivosDespido.objects.all()
    return render(request, 'motivos-despido-listado.html', {'lista':lista})

def motivos_renuncia(request):
    return render(request, 'motivos-renuncia.html')

def motivos_renuncia_editar(request, id):
    dato = MotivosRenuncia.objects.get(pk=id)
    return render(request, 'motivos-renuncia.html', {'editar':True, 'dato':dato})

def motivos_renuncia_listado(request):
    lista = MotivosRenuncia.objects.all()
    return render(request, 'motivos-renuncia-listado.html', {'lista':lista})

def clase_educacion(request):
    return render(request, 'clase-educacion.html')

def clase_educacion_editar(request, id):
    dato = ClaseEducacion.objects.get(pk=id)
    return render(request, 'clase-educacion.html', {'editar':True, 'dato':dato})

def clase_educacion_listado(request):
    lista = ClaseEducacion.objects.all()
    return render(request, 'clase-educacion-listado.html',{'lista':lista})

def educacion(request):
    empleados = Employee.objects.filter(active=True)
    clases_educacion = ClaseEducacion.objects.filter(active=True)
    return render(request, 'educacion.html', {'empleados': empleados, 'clasesEducacion':clases_educacion})

def educacion_editar(request, id):
    empleados = Employee.objects.filter(active=True)
    clases_educacion = ClaseEducacion.objects.filter(active=True)
    dato = Educacion.objects.get(pk=id)
    return render(request, 'educacion.html', {'editar':True, 'dato':dato, 'empleados':empleados, 'clasesEducacion':clases_educacion})

def educacion_listar(request):
    datos = []
    busqueda = None
    empleados = Employee.objects.all()
    if 'empleado' in request.GET:
        emp = request.GET.get("empleado")
        if len(emp) > 0:
            if int(emp) > 0:
                busqueda = int(emp)
                datos = Educacion.objects.filter(empleado__pk=emp)
    return render(request, 'educacion-listado.html', {'datos':datos, 'empleados':empleados, 'busqueda':busqueda})

def evaluacion(request):
    empleados = Employee.objects.filter(active=True)
    return render(request, 'evaluacion.html', {'empleados':empleados})

def evaluacion_listar(request):
    datos = []
    busqueda = None
    empleados = Employee.objects.all()
    if 'empleado' in request.GET:
        emp = request.GET.get("empleado")
        if len(emp) > 0:
            if int(emp) > 0:
                busqueda = int(emp)
                datos = Evaluacion.objects.filter(empleado__pk=emp)
    return render(request, 'evaluaciones-listado.html', {'datos':datos, 'empleados':empleados, 'busqueda': busqueda})



#---------------------------->>>> VISTAS AJAX <<<<----------------------------#
def guardar_empleado(request):
    mensaje = ""
    emp = {}
    oslsPer = None
    obpos = None
    odep = None
    oStatus = None
    oslsPer = None
    obranch = None
    oState = None
    oCountry = None
    oWState = None
    oTermRea = None
    oWCountry = None
    oSex = None
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
                activo = int(request.POST['activo'])
                pos = int(request.POST['pos'])
                telOf = request.POST['telOf']
                dept = int(request.POST['dept'])
                telExt = request.POST['telExt']
                suc = int(request.POST['suc'])
                telMov = request.POST['telMov']
                pag = request.POST['pag']
                slsP = int(request.POST['slsP'])
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
                hdept = int(request.POST['hdept'])
                hpais = int(request.POST['hpais'])
                wcalle = request.POST['wcalle']
                wncalle = request.POST['wncalle']
                wbloque = request.POST['wbloque']
                wedif = request.POST['wedif']
                wcodPos = request.POST['wcodPost']
                wciudad = request.POST['wciudad']
                wcondado = request.POST['wcondado']
                wdept = int(request.POST['wdept'])
                wpais = int(request.POST['wpais'])
                fechaCont = request.POST['fechaCont']
                estEmp = int(request.POST['estEmp'])
                fechaRes = request.POST['fechaRES']
                term = int(request.POST['term'])
                sexo = int(request.POST['sexo'])
                fecNac = request.POST['fecNac']
                lugNac = int(request.POST['lugNac'])
                estCivil = int(request.POST['estCivil'])
                cantHijos = int(request.POST['cantHijos'])
                govID = request.POST['numID']
                citiz = int(request.POST['citiz'])
                numPass = request.POST['numPass']
                fecPassExt = request.POST['fecPassExt']
                fecEmis = request.POST['fecEmis']
                emisor = request.POST['emisor']
                salary = float(request.POST['salario'])
                salaryUnits = int(request.POST['salarioUnd'])
                empCost = float(request.POST['costEmp'])
                empCostUnit = int(request.POST['costEmpUni'])
                banco = int(request.POST['banco'])
                numCuenta = request.POST['numCuenta']
                branchBank = request.POST['bankSucursal']
                remark = request.POST['comentarios']

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if pos > 0:
                    obpos = Position.objects.get(pk=pos)
                if dept > 0:
                    odep = Department.objects.get(pk=dept)
                if suc > 0:
                    obranch = Branch.objects.get(pk=suc)
                if slsP > 0:
                    oslsPer = SalesPerson.objects.get(pk=slsP)
                if hdept > 0:
                    oState = State.objects.get(pk=hdept)
                if hpais > 0:
                    oCountry = Country.objects.get(pk=hpais)
                if wdept > 0:
                    oWState = State.objects.get(pk=wdept)
                if wpais > 0:
                    oWCountry = Country.objects.get(pk=wpais)
                if estEmp > 0:
                    oStatus = StatusEmp.objects.get(pk=estEmp)
                if len(fechaCont) == 0:
                    fechaCont = None
                if len(fechaRes) == 0:
                    fechaRes = None
                if term > 0:
                    oTermRea = TermReason.objects.get(pk=term)
                if sexo > 0:
                    oSex = Sex.objects.get(pk=sexo)
                if len(fecNac) == 0:
                    fecNac = None
                if lugNac > 0:
                    oBirthCountry = Country.objects.get(pk=lugNac)
                if estCivil > 0:
                    oCivilStatus = CivilStatus.objects.get(pk=estCivil)
                if citiz > 0:
                    oCitizenShip = Country.objects.get(pk=citiz)
                if len(fecPassExt) == 0:
                    fecPassExt = None
                if len(fecEmis) == 0:
                    fecEmis = None
                if salaryUnits > 0:
                    oSalaryUnits = SalaryUnit.objects.get(pk=salaryUnits)
                if empCostUnit > 0:
                    oEmpCostUnit = CostUnit.objects.get(pk=empCostUnit)
                if banco > 0:
                    oBankCode = Bank.objects.get(pk=banco)
                
                if len(pNom) > 0 and len(apellido) > 0 and len(puesto) > 0 and len(no_ext) > 0:
                    oEmpleado = Employee(
                        firstName=pNom,
                        middleName = sNom,
                        lastName=apellido,
                        extEmpNo=no_ext,
                        jobTitle=puesto,
                        user_reg=request.user,
                        active = activo,
                        position = obpos,
                        officeTel = telOf,
                        dept = odep,
                        officeExt = telExt,
                        branch = obranch,
                        mobile = telMov,
                        pager = pag,
                        slsPerson = oslsPer,
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
                        homeState = oState,
                        homeCountry = oCountry,
                        workStreet = wcalle,
                        streetNoW = wncalle,
                        workBlock = wbloque,
                        workBuild = wedif,
                        workZip = wcodPos,
                        workCity = wciudad,
                        workCounty = wcondado,
                        workState = oWState,
                        workCountry = oWCountry,
                        startDate = fechaCont,
                        status = oStatus,
                        termDate = fechaRes,
                        termReason = oTermRea,
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
                        salaryUnits = oSalaryUnits,
                        empCost = empCost,
                        empCostUnit = oEmpCostUnit,
                        bankCode = oBankCode,
                        bankAccount = numCuenta,
                        branchBank = branchBank,
                        remark = remark,
                    )
                    oEmpleado.save()
                    emp = {
                        'firstName': oEmpleado.firstName,
                        'lastName': oEmpleado.lastName,
                        'extEmpNo': oEmpleado.extEmpNo,
                        'jobTitel': oEmpleado.jobTitle,
                    }
                    mensaje = 'Se ha guardado el registro del empleado'
                    data = {
                        'empleado':emp, 'mensaje':mensaje, 'error': False
                    }
                else:
                    mensaje = "Complete los campos requeridos."
                    data = {
                        'empleado':emp, 'mensaje':mensaje, 'error': True
                    }
                return JsonResponse(data)
    except Exception as ex:
        data = {
            'error':True,
            'mensaje': 'error',
        }
        print ex
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
                
                if len(razon) > 0:
                    oGrupo = GrupoCorporativo(
                        razonSocial = razon,
                        nombreComercial = nombre,
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

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(nombre) > 0:
                    oSucursal = Branch(
                        name = nombre,
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

                if len(nombre) > 0 and len(desc) > 0:
                    oSucursal = Branch.objects.get(pk=id)

                    if oSucursal:
                        oSucursal.name = nombre
                        oSucursal.description = desc
                        oSucursal.active = activo
                        oSucursal.user_mod = request.user
                        oSucursal.date_mod = datetime.datetime.now()
                        oSucursal.save()
                        sucursal = {
                            'pk': oSucursal.pk,
                            'desc': oSucursal.description,
                            'nombre': oSucursal.name,
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
                descripcion = request.POST['descripcion']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(descripcion) > 0:
                    oDivision = Divisiones(
                        descripcion = descripcion,
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
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oDiv = Divisiones.objects.get(pk=id)

                    if oDiv:
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
                
                if len(nombre) > 0 and len(descripcion) > 0:
                    oDeparment = Department(
                        name = nombre,
                        description = descripcion,
                        active = activo,
                        user_reg=request.user,
                    )
                    oDeparment.save()
                    grupo = {
                        'pk':oDeparment.pk,
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
                        oDep.name = nombre
                        oDep.description = desc
                        oDep.active = activo
                        oDep.user_mod = request.user
                        oDep.date_mod = datetime.datetime.now()
                        oDep.save()
                        dep = {
                            'pk': oDep.pk,
                            'name':oDep.name,
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

                if len(nombre) > 0 and len(descripcion) > 0:
                    oPuesto = Position(
                        name=nombre,
                        description=descripcion,
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
        print ex
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
                
                print activo
                if len(nombre) > 0 and len(desc) > 0:
                    oPos = Position.objects.get(pk=id)

                    if oPos:
                        totReg = Employee.objects.filter(position__pk=id).count()
                        if totReg > 0:
                            oPos.name = nombre
                            oPos.description = desc
                            oPos.active = activo
                            oPos.user_mod = request.user
                            oPos.date_mod = datetime.datetime.now()
                            oPos.save()
                            pos = {
                                'pk': oPos.pk,
                                'name':oPos.name,
                                'desc': oPos.description,
                                'activo': oPos.active,
                            }
                            mensaje = 'Se ha actualizado el registro.'
                            data = {
                                'puesto': pos, 'mensaje': mensaje, 'error': False
                            }
                        else:
                            mensaje = 'El registro tiene datos asociados.'
                            data = {
                                'mensaje': mensaje, 'error': True
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
                descripcion = request.POST['descripcion']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(descripcion) > 0:
                    oCCosto = CentrosCostos(
                        descripcion=descripcion,
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

                if len(nombre) > 0 and len(codigo) > 0:
                    oCountry = Country(
                        code = codigo,
                        name = nombre,
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
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(nombre) > 0 and len(codigo) > 0:
                    oDepto = State(
                        code = codigo,
                        name = nombre,
                        active=activo,
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
                nombre = request.POST['nombre']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(cod) > 0 and len(nombre) > 0:
                    oDept = State.objects.get(pk=id)
                    if oDept:
                        oDept.code = cod
                        oDept.name = nombre
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

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(nombre) > 0 and len(ID) > 0:
                    oCdd = Ciudad(
                        ID_ciudad = ID,
                        nombre = nombre,
                        active=activo,
                        user_reg=request.user,
                    )
                    oCdd.save()
                    ciudad = {
                        'pk': oCdd.pk,
                        'ID': oCdd.ID_ciudad,
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
                        oCdd.ID_ciudad = ID
                        oCdd.nombre = nombre
                        oCdd.active = activo
                        oCdd.user_mod = request.user
                        oCdd.date_mod = datetime.datetime.now()
                        oCdd.save()
                        ciudad = {
                            'pk': oCdd.pk,
                            'ID':oCdd.ID_ciudad,
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
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oGnr = Sex(
                        description = desc,
                        active=activo,
                        user_reg=request.user,
                    )
                    oGnr.save()
                    genero = {
                        'pk': oGnr.pk,
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
                activo = int(request.POST['activo'])

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
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oCv = CivilStatus(
                        description = desc,
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
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

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
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oPr = Parentesco(
                        descripcion = desc,
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
                activo = int(request.POST['activo'])

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
                nombre = request.POST['nombre']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0:
                    oFn = FuncionesTrabajo(
                        nombre = nombre,
                        descripcion = desc,
                        active=activo,
                        user_reg=request.user,
                    )
                    oFn.save()
                    funcion = {
                        'pk': oFn.pk,
                        'nombre': oFn.nombre,
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
                nombre = request.POST['nombre']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(desc) > 0:
                    oFn = FuncionesTrabajo.objects.get(pk=id)
                    if oFn:
                        oFn.nombre = nombre
                        oFn.descripcion = desc
                        oFn.active = activo
                        oFn.user_mod = request.user
                        oFn.date_mod = datetime.datetime.now()
                        oFn.save()
                        funcion = {
                            'pk': oFn.pk,
                            'nombre':oFn.nombre,
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
                nombre = request.POST['nombre']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0 and len(nombre) > 0:
                    oEq = EquipoTrabajo(
                        nombre = nombre,
                        descripcion = desc,
                        active=activo,
                        user_reg=request.user,
                    )
                    oEq.save()
                    equipo = {
                        'pk': oEq.pk,
                        'nombre': oEq.nombre,
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
                nombre = request.POST['nombre']
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(desc) > 0:
                    oMd = EquipoTrabajo.objects.get(pk=id)
                    if oMd:
                        oMd.nombre = nombre
                        oMd.descripcion = desc
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        registro = {
                            'pk': oMd.pk,
                            'nombre':oMd.nombre,
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

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if len(desc) > 0 and len(nombre) > 0:
                    oMd = StatusEmp(
                        name = nombre,
                        description = desc,
                        active=activo,
                        user_reg=request.user,
                    )
                    oMd.save()
                    registro = {
                        'pk': oMd.pk,
                        'nombre': oMd.name,
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
                        oMd.name = nombre
                        oMd.description = desc
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        registro = {
                            'pk': oMd.pk,
                            'nombre':oMd.name,
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
                print "Activo: " + str(activo)
                
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
                    if not validateDateEs(desde):
                        mensaje = 'Ingrese un motivo del ausentismo.'
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

                oMd = Ausentismo(
                    empleado = oEmp,
                    desde = desde,
                    hasta = hasta,
                    motivo = motivo,
                    aprobado = oAprobo,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    'pk': oMd.pk,
                    'empleado': oMd.empleado.pk,
                    'desde': oMd.desde,
                    'hasta': oMd.hasta,
                    'motivo': oMd.motivo,
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
                    mensaje = "Agregue datos al campo 'Motivo'."
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
                    oMd.motivo = motivo
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
                pagado = request.POST['pagado']
                activo = request.POST['activo']
                
                if len(desc) == 0:
                    mensaje = 'Ingrese una descripción.'
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

                oMd = MotivosAusencia(
                    descripcion = desc,
                    pagado = pagado,
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
                nombre = request.POST['nombre']
                activo = request.POST['activo']
                
                if len(nombre) == 0:
                    mensaje = 'El campo "Nombre" es obligatorio.'
                    data = {
                        'mensaje': mensaje, 'error': True
                    }
                    return JsonResponse(data)

                if int(activo) == 1:
                    activo = True
                else:
                    activo = False

                oMd = MotivosDespido(
                    descripcion = desc,
                    nombre = nombre,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    'pk': oMd.pk,
                    'desc': oMd.descripcion,
                    'nombre': oMd.nombre,
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
                nombre = request.POST['nombre']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(desc) > 0:
                    oMd = MotivosDespido.objects.get(pk=id)
                    if oMd:
                        oMd.descripcion = desc
                        oMd.nombre = nombre
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        registro = {
                            'pk': oMd.pk,
                            'descripcion':oMd.descripcion,
                            'nombre': oMd.nombre,
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
                activo = request.POST['activo']
                
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

                oMd = MotivosRenuncia(
                    descripcion = desc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    'pk': oMd.pk,
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
                desc = request.POST['desc']
                activo = int(request.POST['activo'])

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
                            'pk': oMd.pk,
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
                nombre = request.POST['nombre']
                desc = request.POST['desc']
                activo = request.POST['activo']

                if len(nombre) == 0:
                    mensaje = 'El campo "Nombre" es obligatorio.'
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

                oMd = ClaseEducacion(
                    nombre = nombre,
                    descripcion = desc,
                    active=activo,
                    user_reg=request.user,
                )
                oMd.save()
                registro = {
                    'pk': oMd.pk,
                    'nombre': oMd.nombre,
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
                nombre = request.POST['nombre']
                activo = int(request.POST['activo'])

                if activo == 1:
                    activo = True
                else:
                    activo = False
                
                if len(desc) > 0 and len(nombre) > 0:
                    oMd = ClaseEducacion.objects.get(pk=id)
                    if oMd:
                        oMd.nombre = nombre
                        oMd.descripcion = desc
                        oMd.active = activo
                        oMd.user_mod = request.user
                        oMd.date_mod = datetime.datetime.now()
                        oMd.save()
                        registro = {
                            'pk': oMd.pk,
                            'nombre':oMd.nombre,
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

                

                oMd = Educacion(
                    empleado = oEmp,
                    clase_edu = oClsEdu,
                    desde = desde,
                    hasta = hasta,
                    entidad = entidad,
                    asignatura_principal = asignatura,
                    titulo = titulo,
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
