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
    return render(request, 'empleado-form.html', {'positions':positions, 'departments':departments, 'branches':branches, 'salesPersons':salesPersons, 'states':states, 'countries':countries})

def empleado_listado(request):
    empleados = Employee.objects.all()
    return render(request, 'empleado-listado.html', {'empleados':empleados})

def empleado_perfil(request):
    return render(request, 'perfil-empleado.html')

#---------------------------->>>> VISTAS AJAX <<<<----------------------------#
def guardar_empleado(request):
    mensaje = ""
    emp = {}
    if  request.is_ajax():
        if request.method == 'POST':
            primerNombre = request.POST['primerNombre']
            segundoNombre = request.POST['segundoNombre']
            apellido = request.POST['apellido']
            puesto = request.POST['puesto']
            no_ext = request.POST['numExt']
            if len(primerNombre) > 0 and len(apellido) > 0 and len(puesto) > 0 and len(no_ext) > 0:
                oEmpleado = Employee(
                    firstName=primerNombre,
                    middleName = segundoNombre,
                    lastName=apellido,
                    extEmpNo=no_ext,
                    jobTitle=puesto,
                    user_reg=request.user, 
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