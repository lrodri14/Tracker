# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from worksheet.models import *
import datetime

# Create your views here.
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

def listadoCorporativo(request):
    corporativos = GrupoCorporativo.objects.all().order_by('date_reg')
    return render(request, 'corporativo-listado.html', {'corporativos':corporativos})

def empresa(request):
    return render(request, 'empresa.html')

def listadoEmpresa(request):
    empresas = Empresa.objects.all()
    return render(request, 'empresa-listado.html', {'empresas':empresas})

def sucursal(request):
    return render(request, 'sucursal.html')

def listadoSucursal(request):
    sucursales = Branch.objects.all()
    return render(request, 'sucursal-listado.html', {'sucursales':sucursales})

def divisiones(request):
    return render(request, 'divisiones.html')

def listadoDivisiones(request):
    divisiones = Divisiones.objects.all()
    return render(request, 'divisiones-listado.html', {'divisiones':divisiones})

def departamentos(request):
    return render(request, 'departamentos.html')

def listadoDepartamentos(request):
    deptos = Department.objects.all()
    return render(request, 'departamento-listado.html', {'deptos':deptos})

def puestoTrabajo(request):
    return render(request, 'puesto-trabajo.html')



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