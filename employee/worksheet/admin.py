# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Permission
from django.contrib import admin
from worksheet.models import *

admin.site.site_header = "Tracker"
admin.site.title = "Tracker"

@admin.register(EmpleadoDeducciones)
class EmpleadoDeduccionesAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'deduccion', 'active']


# Register your models here.
admin.site.register(ActivoAsignado)
admin.site.register(Ausentismo)
admin.site.register(Bank)
admin.site.register(Branch)
admin.site.register(CentrosCostos)
admin.site.register(Ciudad)
admin.site.register(CivilStatus)
admin.site.register(ClaseEducacion)
admin.site.register(CostUnit)
admin.site.register(Country)
admin.site.register(Department)
admin.site.register(DeduccionGeneral)
admin.site.register(DeduccionGeneralDetalle)
admin.site.register(DeduccionIndividual)
admin.site.register(DeduccionIndividualDetalle)
admin.site.register(DeduccionIndividualPlanilla)
admin.site.register(Employee)
admin.site.register(EncabezadoImpuestoSobreRenta)
admin.site.register(LimiteSalarioDeduccion)
admin.site.register(Empresa)
admin.site.register(Evaluacion)
admin.site.register(Group)
admin.site.register(GrupoCorporativo)
admin.site.register(ImagenEmpleado)
admin.site.register(ImpuestoSobreRenta)
admin.site.register(ImpuestoVecinal)
admin.site.register(IncrementosSalariales)
admin.site.register(IngresoIndividual)
admin.site.register(IngresoGeneral)
admin.site.register(IngresoGeneralDetalle)
admin.site.register(IngresoIndividualDetalle)
admin.site.register(IngresoIndividualPlanilla)
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
