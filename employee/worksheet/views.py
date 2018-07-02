# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from worksheet.models import *

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
    return render(request, 'empleado-form.html', {'positions':positions, 'departments':departments, 'branches':branches, 'salesPersons':salesPersons, 'states':states, 'countries':countries, 'stats':estados_emp, 'terms':terms})

def empleado_listado(request):
    empleados = Employee.objects.all()
    return render(request, 'empleado-listado.html', {'empleados':empleados})

def empleado_perfil(request):
    return render(request, 'perfil-empleado.html')

#---------------------------->>>> VISTAS AJAX <<<<----------------------------#
def guardar_empleado(request):
    mensaje = ""
    emp = {}
    oslsPer = None
    obpos = None
    odep = None
    oslsPer = None
    obranch = None
    oState = None
    oCountry = None
    oWState = None
    oWCountry = None
    try:
        if  request.is_ajax():
            if request.method == 'POST':
                primerNombre = request.POST['primerNombre']
                segundoNombre = request.POST['segundoNombre']
                apellido = request.POST['apellido']
                puesto = request.POST['puesto']
                no_ext = request.POST['numExt']
                activo = int(request.POST['activo'])
                posicion = int(request.POST['posicion'])
                dept = int(request.POST['departamento'])
                branch = int(request.POST['sucursal'])
                slsPerson = int(request.POST['empVentas'])
                officeTel = request.POST['telOficina']
                officeExt = request.POST['extOficina']
                mobile = request.POST['celular']
                pager = request.POST['pager']
                homeTel = request.POST['telCasa']
                fax = request.POST['fax']
                email = request.POST['correo']
                homeStreet = request.POST['calle']
                streetNoH = request.POST['num_calle']
                homeBuild = request.POST['edificio']
                homeZip = request.POST['codigo_postal']
                homeBlock = request.POST['bloque']
                homeCity = request.POST['ciudad']
                homeCounty = request.POST['condado']
                homeState = int(request.POST['estado'])
                homeCountry = int(request.POST['pais'])
                workStreet = request.POST['wcalle']
                streetNoW = request.POST['wnum_calle']
                workBuild = request.POST['wedificio']
                workZip = request.POST['wcodigo_postal']
                workBlock = request.POST['wbloque']
                workCity = request.POST['wciudad']
                workCounty = request.POST['wcondado']
                workState = int(request.POST['westado'])
                workCountry = int(request.POST['wpais'])

                if activo == 1:
                    activo = True
                else:
                    activo = False

                if posicion > 0:
                    obpos = Position.objects.get(pk=posicion)
                if dept > 0:
                    odep = Department.objects.get(pk=dept)
                if slsPerson > 0:
                    oslsPer = SalesPerson.objects.get(pk=slsPerson)
                if branch > 0:
                    obranch = Branch.objects.get(pk=branch)
                if homeState > 0:
                    oState = State.objects.get(pk=homeState)
                if homeCountry > 0:
                    oCountry = Country.objects.get(pk=homeCountry)
                if workState > 0:
                    oWState = State.objects.get(pk=workState)
                if workCountry > 0:
                    oWCountry = Country.objects.get(pk=workCountry)

                if len(primerNombre) > 0 and len(apellido) > 0 and len(puesto) > 0 and len(no_ext) > 0:
                    oEmpleado = Employee(
                        firstName=primerNombre,
                        middleName = segundoNombre,
                        lastName=apellido,
                        extEmpNo=no_ext,
                        jobTitle=puesto,
                        user_reg=request.user,
                        active = activo,
                        position = obpos,
                        dept = odep,
                        branch = obranch,
                        slsPerson = oslsPer,
                        officeTel = officeTel,
                        officeExt = officeExt,
                        mobile = mobile,
                        pager = pager,
                        homeTel = homeTel,
                        fax = fax,
                        email = email,
                        homeStreet = homeStreet,
                        streetNoH = streetNoH,
                        homeBuild = homeBuild,
                        homeBlock = homeBlock,
                        homeZip = homeZip,
                        homeCity = homeCity,
                        homeCounty = homeCounty,
                        homeState = oState,
                        homeCountry = oCountry,
                        workStreet = workStreet,
                        streetNoW = streetNoW,
                        workBuild = workBuild,
                        workBlock = workBlock,
                        workZip = workZip,
                        workCity = workCity,
                        workCounty = workCounty,
                        workState = oWState,
                        workCountry = oWCountry,
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
            'mensaje': ex,
        }
        return JsonResponse(data)