# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Permission
from django.contrib import admin
from .models import *

admin.site.site_header = "Tracker"
admin.site.title = "Tracker"

@admin.register(EmpleadoDeducciones)
class EmpleadoDeduccionesAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'deduccion', 'active']

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['extEmpNo', 'firstName', 'middleName', 'lastName', 'govID']
    search_fields = ['extEmpNo', 'firstName', 'middleName', 'lastName', 'govID']

class DatosSalarioAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'fecha_incremento']
    search_fields = ['empleado__firstName']

class DeduccionIndividualDetalleAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'deduccion', 'valor', 'date_reg', 'sucursal_reg']
    list_filter = ('deduccion', 'sucursal_reg')
    search_fields = ['empleado__govID', 'empleado__firstName', 'empleado__middleName', 'empleado__lastName']

class DeduccionIndividualPlanillaAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'planilla', 'deduccion', 'valor', 'date_reg', 'sucursal_reg']
    list_filter = ('deduccion', 'sucursal_reg')
    search_fields = ['empleado__govID', 'empleado__firstName', 'empleado__middleName', 'empleado__lastName']

class DeduccionEmpleadoAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'planilla', 'deduccion', 'monto', 'date_reg']
    list_filter = ('planilla', 'empleado','deduccion')
    search_fields = ['empleado__govID', 'empleado__firstName', 'empleado__middleName', 'empleado__lastName']

# class DetallePlanillaDetalleDeduccionAdmin(admin.ModelAdmin):
#     pass
    #list_display = ['planilla_detalle_ded', 'deduccion_detalle']
    #list_filter = ('sucursal_reg',)
    #search_fields = ['deduccion_detalle__empleado__firstName']

# Register your models here.
admin.site.register(ActivoAsignado)
admin.site.register(Ausentismo)
admin.site.register(Bank)
admin.site.register(Branch)
admin.site.register(CentrosCostos)
admin.site.register(Ciudad)
admin.site.register(CivilStatus)
admin.site.register(ClaseEducacion)
admin.site.register(Contrato)
admin.site.register(CostUnit)
admin.site.register(Country)
admin.site.register(ControlPagosDeduccionIndividual)
admin.site.register(CuentaContableAsignacion)
admin.site.register(Department)
#admin.site.register(DetallePlanillaDetalleDeduccion, DetallePlanillaDetalleDeduccionAdmin)
admin.site.register(DeduccionGeneral)
admin.site.register(DeduccionGeneralDetalle)
admin.site.register(DeduccionIndividual)
admin.site.register(DeduccionIndividualDetalle, DeduccionIndividualDetalleAdmin)
admin.site.register(DeduccionIndividualSubDetalle)
admin.site.register(DeduccionIndividualPlanilla, DeduccionIndividualPlanillaAdmin)
admin.site.register(DeduccionTipo)
admin.site.register(DeduccionEmpleado, DeduccionEmpleadoAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EncabezadoImpuestoSobreRenta)
admin.site.register(LimiteSalarioDeduccion)
admin.site.register(Empresa)
admin.site.register(Evaluacion)
admin.site.register(Group)
admin.site.register(GrupoCorporativo)
admin.site.register(HoraExtra)
admin.site.register(ImagenEmpleado)
admin.site.register(ImpuestoSobreRenta)
admin.site.register(ImpuestoVecinal)
admin.site.register(IncrementosSalariales, DatosSalarioAdmin)
admin.site.register(IngresoIndividual)
admin.site.register(IngresoGeneral)
admin.site.register(IngresoGeneralDetalle)
admin.site.register(IngresoIndividualDetalle)
admin.site.register(IngresoIndividualPlanilla)
admin.site.register(IngresoTipo)
admin.site.register(IngresoEmpleado)
admin.site.register(Planilla)
admin.site.register(PlanillaDetalle)
admin.site.register(PlanillaDetalleDeducciones)
admin.site.register(PlanillaDetalleIngresos)
admin.site.register(Permission)
admin.site.register(Position)
admin.site.register(RapDeduccion)
admin.site.register(SalaryUnit)
admin.site.register(SalesPerson)
admin.site.register(SeguroSocial)
admin.site.register(SeguroSocialAjuste)
admin.site.register(Sex)
admin.site.register(State)
admin.site.register(StatusEmp)
admin.site.register(TermReason)
admin.site.register(TipoDeduccion)
admin.site.register(TipoIngreso)
admin.site.register(TipoNomina)
admin.site.register(UsuarioSucursal)
admin.site.register(UsuarioEmpresa)
admin.site.register(UsuarioCorporacion)
admin.site.register(Vendedor)
