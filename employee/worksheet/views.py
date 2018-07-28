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
