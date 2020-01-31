# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

from django.db import models

# Create your models here.

class GrupoCorporativo(models.Model):
    razonSocial = models.CharField(max_length=100, blank=True, null=True)
    nombreComercial = models.CharField(max_length=100, blank=True, null=True)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='gcom_usermod', related_query_name='gcom_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    class Meta:
        verbose_name = "Grupo Corporativo"
        verbose_name_plural = "Grupos Corporativos"

    def __str__(self):
        return self.nombreComercial

class Group(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='grp_usermod', related_query_name='grp_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Empresa(models.Model):
    razonSocial = models.CharField(max_length=100, blank=True, null=True)
    nombreComercial = models.CharField(max_length=100, blank=True, null=True)
    grupo = models.ForeignKey(GrupoCorporativo, blank=True, null=True, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='empr_usermod', related_query_name='empr_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nombreComercial

class Branch(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    description = models.CharField(max_length=250)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='brn_usermod', related_query_name='brn_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __str__(self):
        return self.description

class FuncionesTrabajo(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="fun_empreg", related_query_name="fun_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='fnT_usermod', related_query_name='fnT_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.descripcion

class Position(models.Model):
    code = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=250)
    funcion_operativa = models.ForeignKey("worksheet.FuncionesTrabajo", verbose_name=("Funcion Operativa"), on_delete=models.PROTECT, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="pos_empreg", related_query_name="pos_empreg")
    active = models.BooleanField(default=True)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='pos_usermod', related_query_name='pos_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.description

class Department(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    description = models.CharField(max_length=250)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="dep_empreg", related_query_name="dep_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='dep_usermod', related_query_name='dep_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.description	

class SalesPerson(models.Model):
    slpName = models.CharField(max_length=150)
    groupCode = models.ForeignKey(Group, blank=True, null=True, on_delete=models.PROTECT)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="slsp_empreg", related_query_name="slsp_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="usermod", related_query_name="usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.slpName

class Country(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    name = models.CharField(max_length=150)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING,
                                    related_name="country_empreg", related_query_name="country_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name="country_usermod", related_query_name="country_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class State(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    name = models.CharField(max_length=150)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="state_empreg", related_query_name="state_empreg")
    pais = models.ForeignKey(Country, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="state_pais", related_query_name="state_pais")
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="state_usermod", related_query_name="state_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class StatusEmp(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    description = models.TextField()
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="stemp_empreg", related_query_name="stemp_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="sts_usermod", related_query_name="sts_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

class TermReason(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    description = models.TextField()
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="termres_empreg", related_query_name="termres_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="trm_usermod", related_query_name="trm_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

class Sex(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    description = models.CharField(max_length=25)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="sex_empreg", related_query_name="sex_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="sex_usermod", related_query_name="sex_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

class CivilStatus(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    description = models.CharField(max_length=50)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="cvlstatus_empreg", related_query_name="cvlstatus_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="civStatus_usermod", related_query_name="civStatus_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

class SalaryUnit(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    description = models.TextField()
    dias_salario = models.IntegerField(blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="slrunt_empreg", related_query_name="slrunt_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="salary_usermod", related_query_name="salary_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

class CostUnit(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    description = models.TextField()
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="cstunt_empreg", related_query_name="cstunt_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="cost_usermod", related_query_name="cost_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

class Bank(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    description = models.TextField()
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="bank_empreg", related_query_name="bank_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="bank_usermod", related_query_name="bank_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

class GrupoComisiones(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=150)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="gpCom_empreg", related_query_name="gpCom_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='grpcom_usermod', related_query_name='grpcom_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __str__(self):
        return self.descripcion

class Vendedor(models.Model):
    nombre = models.CharField(max_length=150)
    grupo_comisiones = models.ForeignKey(GrupoComisiones, on_delete=models.PROTECT)
    porcentaje_comision = models.CharField(
        max_length=15, blank=True, null=True)
    telefono = models.CharField(max_length=25, blank=True, null=True)
    tel_movil = models.CharField(max_length=25)
    correo = models.CharField(max_length=150)
    comentario = models.TextField(blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="vendedor_empreg", related_query_name="vendedor_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='vendedor_usermod', related_query_name='vendedor_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.nombre

class TipoNomina(models.Model):
    tipo_planilla = models.CharField(max_length=100)
    descripcion = models.TextField()
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name='tnom_usermod', related_query_name='tnom_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __str__(self):
        return self.tipo_planilla

class TipoContrato(models.Model):
    tipo_contrato = models.CharField(max_length=100)
    descripcion = models.TextField()
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,related_name='tcon_usermod', related_query_name='tcon_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __str__(self):
        return self.tipo_contrato

class Employee(models.Model):
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50, blank=True, null=True)
    lastName = models.CharField(max_length=50)
    extEmpNo = models.CharField(max_length=15, blank=True, null=True)
    jobTitle = models.CharField(max_length=50)
    position = models.ForeignKey(Position, help_text="Posición del empleado", verbose_name="Posicion", blank=True, null=True, on_delete=models.PROTECT)
    dept = models.ForeignKey(Department, blank=True, null=True, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, blank=True, null=True, on_delete=models.PROTECT)
    jefe = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT)
    slsPerson = models.ForeignKey(Vendedor, blank=True, null=True, on_delete=models.PROTECT)
    officeTel = models.CharField(max_length=50, blank=True, null=True)
    officeExt = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    homeTel = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    socialNetwork1 = models.CharField(("Red Social 1"), max_length=250, blank=True, null=True)
    socialNetwork2 = models.CharField(("Red Social 2"), max_length=250, blank=True, null=True)
    #picture = models.ImageField(upload_to='images/emp_photos')
    homeStreet = models.CharField(max_length=250, blank=True, null=True)
    streetNoH = models.CharField(max_length=50, blank=True, null=True)
    homeBuild = models.CharField(max_length=50, blank=True, null=True)
    homeBlock = models.CharField(max_length=50, blank=True, null=True)
    homeZip = models.CharField(max_length=50, blank=True, null=True)
    homeCity = models.CharField(max_length=100, blank=True, null=True)
    homeCounty = models.CharField(max_length=100, blank=True, null=True)
    homeState = models.ForeignKey(State, blank=True, null=True, on_delete=models.SET_NULL, related_name='home_state', related_query_name='home_state')
    homeCountry = models.ForeignKey(Country, blank=True, null=True, on_delete=models.SET_NULL, related_name='home_country', related_query_name='home_country')
    lat = models.CharField(("Latitud"), max_length=350, blank=True, null=True)
    lng = models.CharField(("Longitud"), max_length=350, blank=True, null=True)
    workStreet = models.CharField(max_length=250, blank=True, null=True)
    streetNoW = models.CharField(max_length=50, blank=True, null=True)
    workBlock = models.CharField(max_length=50, blank=True, null=True)
    workBuild = models.CharField(max_length=50, blank=True, null=True)
    workZip = models.CharField(max_length=50, blank=True, null=True)
    workCity = models.CharField(max_length=100, blank=True, null=True)
    workCounty = models.CharField(max_length=100, blank=True, null=True)
    workState = models.ForeignKey(State, blank=True, null=True, on_delete=models.SET_NULL, related_name='work_state', related_query_name='work_state')
    workCountry = models.ForeignKey(Country, blank=True, null=True, on_delete=models.SET_NULL, related_name='work_country', related_query_name='work_country')

    startDate = models.DateField(blank=True, null=True)
    status = models.ForeignKey(StatusEmp, blank=True, null=True, on_delete=models.PROTECT)
    termDate = models.DateField(blank=True, null=True)
    termReason = models.ForeignKey(TermReason, blank=True, null=True, on_delete=models.PROTECT)

    sex = models.ForeignKey(Sex, blank=True, null=True, on_delete=models.PROTECT)
    birthDate = models.DateField(blank=True, null=True)
    birthCountry = models.ForeignKey(Country, blank=True, null=True, on_delete=models.PROTECT)
    marrStatus = models.ForeignKey(CivilStatus, blank=True, null=True, on_delete=models.PROTECT)
    nChildren = models.CharField(max_length=12 ,blank=True, null=True)
    govID = models.CharField(max_length=50, blank=True, null=True)
    citizenship = models.ForeignKey(Country, blank=True, null=True, related_name='citizenship', related_query_name='citizenship', on_delete=models.PROTECT)
    passportNo = models.CharField(max_length=50, blank=True, null=True)
    passportExt = models.DateField(blank=True, null=True)
    passIssue = models.DateField(blank=True, null=True)
    passIssuer = models.CharField(max_length=150, blank=True, null=True)
    rtn = models.CharField(("R.T.N."), max_length=100, blank=True, null=True)

    salary = models.CharField(max_length=20, blank=True, null=True)
    salario_diario = models.CharField(max_length=20, blank=True, null=True)
    salaryUnits = models.ForeignKey(SalaryUnit, blank=True, null=True, on_delete=models.PROTECT)
    empCost = models.CharField(max_length=20, blank=True, null=True)
    empCostUnit = models.ForeignKey(CostUnit, blank=True, null=True, on_delete=models.PROTECT)
    bankCode = models.ForeignKey(Bank, blank=True, null=True, on_delete=models.PROTECT)
    bankAccount = models.CharField(max_length=50, blank=True, null=True)
    branchBank = models.CharField(max_length=150, blank=True, null=True)
    metodo_pago = models.IntegerField(("Metodo de Pago"), blank=True, null=True)
    tipo_nomina = models.ForeignKey("worksheet.TipoNomina", verbose_name="tipo nomina", on_delete=models.PROTECT, blank=True, null=True)
    tipo_contrato = models.ForeignKey("worksheet.TipoContrato", verbose_name="tipo contrato", on_delete=models.PROTECT, blank=True, null=True)

    remark = models.TextField(blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="empl_empreg", related_query_name="empl_empreg")


    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='emp_usermod', related_query_name='emp_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.firstName + " " + self.lastName

    # def __str__(self):
    #     return self.firstName + ' ' + self.lastName

class Divisiones(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="div_empreg", related_query_name="div_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='div_usermod', related_query_name='div_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.descripcion

class CentrosCostos(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="cc_empreg", related_query_name="cc_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='cc_usermod', related_query_name='cc_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.descripcion

class Ciudad(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    nombre = models.CharField(max_length=150)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="ciudad_empreg", related_query_name="ciudad_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='cdd_usermod', related_query_name='cdd_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.nombre

class Parentesco(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="parent_empreg", related_query_name="parent_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='parnt_usermod', related_query_name='parnt_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.descripcion

class EquipoTrabajo(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="eqtr_empreg", related_query_name="eqtr_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='eqTr_usermod', related_query_name='eqTr_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.descripcion

class MotivosAusencia(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=150)
    pagado = models.BooleanField()
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="motIng_empreg", related_query_name="motIng_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='catIng_usermod', related_query_name='catIng_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.descripcion

class Ausentismo(models.Model):
    empleado = models.ForeignKey("worksheet.Employee", on_delete=models.PROTECT)
    desde = models.DateField(blank=True, null=True)
    hasta = models.DateField(blank=True, null=True)
    motivo = models.ForeignKey(MotivosAusencia, blank=True, null=True, on_delete=models.DO_NOTHING)
    aprobado = models.ForeignKey(Employee, related_name='au_emp', related_query_name='au_emp', blank=True, null=True, on_delete=models.PROTECT)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="au_empreg", related_query_name="au_empreg")
    sucursal_reg = models.ForeignKey("worksheet.Branch", on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='au_usermod', related_query_name='au_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.empleado.firstName + ' ' + self.empleado.lastName + ' - ' + str(self.desde) + ' | ' + str(self.hasta)

class MotivosDespido(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="mDes_empreg", related_query_name="mDes_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='mDes_usermod', related_query_name='mDes_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.descripcion

class MotivosRenuncia(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=150)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="mRe_empreg", related_query_name="mRe_empreg")
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='mRe_usermod', related_query_name='mRe_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.descripcion

class ClaseEducacion(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="clsEd_empreg", related_query_name="clsEd_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='clsEdu_usermod', related_query_name='clsEdu_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.descripcion

class Educacion(models.Model):
    empleado = models.ForeignKey(Employee, on_delete=models.PROTECT)
    desde = models.DateField()
    hasta = models.DateField()
    clase_edu = models.ForeignKey(ClaseEducacion, blank=True, null=True, on_delete=models.SET_NULL)
    entidad = models.CharField(max_length=100, blank=True, null=True)
    asignatura_principal = models.CharField(max_length=100, blank=True, null=True)
    titulo = models.CharField(max_length=100, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="Ed_empreg", related_query_name="Ed_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='edu_usermod', related_query_name='edu_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.empleado.firstName + ' ' + self.empleado.lastName + ' | ' + self.clase_edu.nombre

class Evaluacion(models.Model):
    empleado = models.ForeignKey(Employee, on_delete=models.PROTECT)
    fecha = models.DateField()
    descripcion = models.TextField()
    gerente = models.ForeignKey(Employee,  blank=True, null=True, on_delete=models.SET_NULL, related_name='eV_gerente', related_query_name="eV_gerente")
    grupo_salarial = models.CharField(max_length=100)
    comentario = models.TextField()
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="eV_empreg", related_query_name="eV_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='eV_usermod', related_query_name='eV_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.empleado.firstName + ' ' + self.empleado.lastName + ' | ' + str(self.fecha)

class MotivoAumentoSueldo(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=150)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="mAuSal_empreg", related_query_name="mAuSal_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name='mAuSal_usermod', related_query_name='mAuSal_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.descripcion

class EmpleosAnteriores(models.Model):
    empleado = models.ForeignKey(Employee, on_delete=models.PROTECT)
    desde = models.DateField()
    hasta = models.DateField()
    empresa = models.CharField(max_length=100, blank=True, null=True)
    posicion = models.CharField(max_length=100, blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="empAnt_empreg", related_query_name="empAnt_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='empAnt_usermod', related_query_name='empAnt_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.empleado.firstName

class Banco(models.Model):
    pais = models.ForeignKey(Country, on_delete=models.PROTECT)
    codigo = models.CharField(max_length=15)
    nombre = models.CharField(max_length=100)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="Banco_empreg", related_query_name="Banco_empreg")
    bic_swift = models.CharField(max_length=100, blank=True, null=True)
    of_postal = models.BooleanField()
    cuenta_bancaria = models.CharField(max_length=100)
    sucursal = models.CharField(max_length=100)
    
    def __str__(self):
        return self.codigo + ' ' + self.nombre + ' ' + self.pais.name

class Feriado(models.Model):
    fecha = models.DateField()
    rate = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=150)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="feriado_empreg", related_query_name="feriado_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='fer_usermod', related_query_name='fer_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        return str(self.fecha)

class ActivoAsignado(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=150)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="actasig_empreg", related_query_name="actasig_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='actasig_usermod', related_query_name='actasig_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __str__(self):
        return self.descripcion
    
class UsuarioEmpresa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='usemp_user', related_query_name='usemp_user')
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='usemp_usermod', related_query_name='usemp_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __str__(self):
        return self.usuario.username + " - " + self.empresa.nombreComercial

class UsuarioSucursal(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='usbranch_user', related_query_name='usbranch_user')
    sucursal = models.ForeignKey(Branch, blank=True, null=True, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='usbranc_usermod', related_query_name='usbranch_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __str__(self):
        return self.usuario.username + " - " + self.sucursal.description

class ImagenEmpleado(models.Model):
    empleado = models.OneToOneField("worksheet.employee", verbose_name="Empleado", on_delete=models.DO_NOTHING)
    imagen = models.ImageField(upload_to='images/emp_photos')
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="imgemp_empreg", related_query_name="imgemp_empreg")
    user_reg = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='imgemp_usermod', related_query_name='imgemp_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)
    
    def __str__(self):
        return self.empleado.firstName + " " + self.empleado.lastName

class TipoDeduccion(models.Model):
    IHSS = 'IHSS'
    RAP = 'RAP'
    ISR = 'ISR'
    IMV = 'IMV'
    INTERNAS = 'DEDUCCIONES INTERNAS'
    EXTERNAS = 'DEDUCCIONES EXTERNAS'
    TIPOS = [
        (IHSS, 'IHSS'),
        (IMV, 'IMPUESTO VECINAL'),
        (ISR, 'ISR'),
        (RAP, 'RAP'),
        (INTERNAS, 'DEDUCCIONES INTERNAS'),
        (EXTERNAS, 'DEDUCCIONES EXTERNAS')
    ]
    tipo_deduccion = models.CharField(max_length=50)
    descripcion = models.TextField()
    grupo = models.CharField(("Grupo"), max_length=20, choices=TIPOS, blank=True, null=True)
    orden = models.CharField(("Orden"), max_length=50, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='tded_usermod', related_query_name='tded_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Tipo Deduccion"
        verbose_name_plural = "Tipo Deducciones"

    def __str__(self):
        return self.tipo_deduccion + " - " + str(self.orden)

class TipoIngreso(models.Model):
    SALARIO = 'SALARIOS'
    BONO = 'BONOS'
    VACACIONES = 'VACACIONES'
    DIA_LIBRE = 'DÍAS LIBRES'
    OTROS = 'OTROS INGRESOS'
    TIPOS = [
        (SALARIO, 'SALARIOS'),
        (BONO, 'BONOS'),
        (DIA_LIBRE, 'DÍAS LIBRES'),
        (OTROS, 'OTROS INGRESOS'),
        (VACACIONES, 'VACACIONES'),
    ]
    grupo = models.CharField(("Grupo"), max_length=20, choices=TIPOS, blank=True, null=True)
    tipo_ingreso = models.CharField(max_length=50)
    descripcion = models.TextField()
    orden = models.CharField(("Orden"), max_length=50, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='ting_usermod', related_query_name='ting_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __str__(self):
        return self.tipo_ingreso + " - " + str(self.orden)

class IngresoIndividual(models.Model):
    ingreso_i = models.CharField(max_length=50)
    tipo_ingreso = models.ForeignKey(TipoIngreso, on_delete=models.PROTECT)
    gravable = models.BooleanField()
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey(Branch, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name='ingind_usermod', related_query_name='ingind_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField()

    def __str__(self):
        return self.ingreso_i

class IngresoGeneral(models.Model):
    ingreso_g = models.CharField(max_length=50)
    tipo_ingreso = models.ForeignKey("worksheet.TipoIngreso", verbose_name="tipo ingreso", on_delete=models.PROTECT)
    gravable = models.BooleanField()
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey(Branch, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name='ingg_usermod', related_query_name='ingg_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField()

    def __str__(self):
        return self.ingreso_g

class DeduccionIndividual(models.Model):
    deduccion_i = models.CharField(max_length=50)
    tipo_deduccion = models.ForeignKey("worksheet.TipoDeduccion", verbose_name="deduccion individual", on_delete=models.PROTECT)
    control_saldo = models.BooleanField(default=True)
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey(Branch, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name='dedind_usermod', related_query_name='dedind_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField()

    class Meta:
        verbose_name = "Deduccion Individual"
        verbose_name_plural = "Deducciones Individuales"

    def __str__(self):
        return 'Model: %s' % self.deduccion_i

    # def __str__(self):
    #     return self.deduccion_i

class DeduccionGeneral(models.Model):
    deduccion_g = models.CharField(max_length=50)
    tipo_deduccion = models.ForeignKey("worksheet.TipoDeduccion", verbose_name="tipo deduccion", on_delete=models.PROTECT)
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey(Branch, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name='deg_usermod', related_query_name='deg_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField()
    
    class Meta:
        verbose_name = "Deduccion General"
        verbose_name_plural = "Deduccion Generales"

    def __str__(self):
        return self.deduccion_g

#Transacciones
class IncrementosSalariales(models.Model):
    empleado = models.ForeignKey("worksheet.employee", verbose_name="Empleado", on_delete=models.DO_NOTHING)
    fecha_incremento = models.DateField()
    motivo_aumento = models.ForeignKey(MotivoAumentoSueldo, on_delete=models.DO_NOTHING)
    salario_anterior = models.DecimalField(max_digits=18, decimal_places=4)
    incremento = models.DecimalField(max_digits=18, decimal_places=4)
    nuevo_salario = models.DecimalField(max_digits=18, decimal_places=4)
    comentarios = models.TextField(blank=True, null=True)
    salario_actual = models.BooleanField(blank=False, null=False, default=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING)
    user_reg = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='incsal_usermod', related_query_name='incsal_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __str__(self):
        return self.empleado.firstName + ' ' + self.empleado.lastName + ' | ' + str(self.fecha_incremento)

@receiver(post_save, sender=IncrementosSalariales)
def post_save_incrementossalariales(sender, instance, **kwargs):
    if kwargs['created']:
        tot_reg = IncrementosSalariales.objects.filter(empleado=instance.empleado, active=True, salario_actual=True).count()
        if tot_reg > 0:
            datos = IncrementosSalariales.objects.filter(empleado=instance.empleado, active=True, salario_actual=True).exclude(pk=instance.pk)
            if datos.count() > 0:
                dato = datos[0]
                dato.salario_actual=False
                dato.user_mod = instance.user_reg
                dato.date_mod = datetime.datetime.now()
                dato.save()
                
        d_empleado = Employee.objects.get(pk=instance.empleado.pk)
        d_empleado.salary = str(instance.nuevo_salario)
        d_empleado.salario_diario = float(instance.nuevo_salario) / float(30)
        # if d_empleado.salaryUnits:
        #     tot_reg = SalaryUnit.objects.filter(pk=d_empleado.salaryUnits.pk).count()
        #     if tot_reg > 0:
        #         o_salary_units = SalaryUnit.objects.get(pk=d_empleado.salaryUnits.pk)
        #         if o_salary_units.dias_salario > 0:
        #             d_empleado.salario_diario = float(instance.nuevo_salario) / float(o_salary_units.dias_salario)
        d_empleado.save()

class EncabezadoImpuestoSobreRenta(models.Model):
    codigo = models.CharField(("Codigo"), max_length=50)
    fecha_vigencia = models.DateField(("Fecha vigencia"), blank=True, null=True)
    descripcion = models.CharField(("Descripción"), max_length=150, blank=True, null=True)
    valor = models.DecimalField(("Valor"), max_digits=18, decimal_places=4, blank=True, null=True)
    descripcion1 = models.CharField(("Descripcion 1"), max_length=150, blank=True, null=True)
    valor1 = models.DecimalField(("Valor 1"), max_digits=18, decimal_places=4, blank=True, null=True)
    descripcion2 = models.CharField(("Descripcion 2"), max_length=150, blank=True, null=True)
    valor2 = models.DecimalField(("Valor 2"), max_digits=18, decimal_places=4, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING)
    user_reg = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='isr_enc_usermod', related_query_name='isr_enc_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    class Meta:
        verbose_name = ("EncabezadoImpuestoSobreRenta")
        verbose_name_plural = ("EncabezadoImpuestoSobreRentas")

    def __str__(self):
        return self.codigo

class ImpuestoSobreRenta(models.Model):
    desde = models.DecimalField(max_digits=15, decimal_places=2)
    hasta = models.DecimalField(max_digits=15, decimal_places=2)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    porcentaje_label = models.CharField(max_length=50)
    encabezado = models.ForeignKey("worksheet.EncabezadoImpuestoSobreRenta", verbose_name=("ISR"), on_delete=models.PROTECT, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING)
    user_reg = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='isv_usermod', related_query_name='isv_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)
    
    class Meta:
        verbose_name ="impuesto sobre renta"
        verbose_name_plural = "impuestos sobre rentas"

    def __str__(self):
        return self.porcentaje_label

class SeguroSocial(models.Model):
    tipo = models.CharField(max_length=50)
    techo = models.CharField(max_length=70)
    porcentaje_e = models.CharField(max_length=50)
    valor_e = models.CharField(max_length=50)
    porcentaje_p = models.CharField(max_length=50)
    valor_p = models.CharField(max_length=50)
    total_p = models.CharField(max_length=50)
    total_v = models.CharField(max_length=50)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='ss_usermod', related_query_name='ss_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    class Meta:
        verbose_name = "Seguro Social"
        verbose_name_plural = "Seguro Social"

    def __str__(self):
        return self.tipo

class ImpuestoVecinal(models.Model):
    desde = models.DecimalField(max_digits=18, decimal_places=2)
    hasta = models.DecimalField(max_digits=18, decimal_places=2)
    porcentaje = models.DecimalField(max_digits=18, decimal_places=2)
    porcentaje_label = models.CharField(max_length=50)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='iv_usermod', related_query_name='iv_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)
    
    class Meta:
        verbose_name = ("Impuesto Vecinal")
        verbose_name_plural = ("Impuestos Vecinales")

    def __str__(self):
        return "%s | %s"%(self.date_reg, self.porcentaje_label)

class HoraExtra(models.Model):
    jornada = models.CharField(("Jornada"), max_length=50)
    horaini = models.TimeField(("Hora Inicial"), auto_now=False, auto_now_add=False)
    horafin = models.TimeField(("Hora Fin"), auto_now=False, auto_now_add=False)
    horasDiarias = models.DecimalField(("Horas Diarias"), max_digits=10, decimal_places=2)
    horasSemana = models.DecimalField(("Horas Semana"), max_digits=10, decimal_places=2)
    noExedeNocturno = models.IntegerField()
    horaExtra = models.DecimalField(("Hora Extra"), max_digits=10, decimal_places=2)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='he_usermod', related_query_name='he_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    class Meta:
        verbose_name = ("Hora Extra")
        verbose_name_plural = ("Horas Extras")

    def __str__(self):
        return self.jornada

class SalarioMinimo(models.Model):
    fecha = models.DateField(("Fecha"), auto_now_add=True)
    salario_minimo = models.DecimalField(("Salario Minimo"), max_digits=18, decimal_places=4)
    forzar_salario = models.NullBooleanField(("Forzar salario"))
    vigente = models.BooleanField(("Vigente"))
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey(Branch, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name='sm_usermod', related_query_name='sm_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField()

    class Meta:
        verbose_name = ("Salario Minimo")
        verbose_name_plural = ("Salario Minimo")

    def __str__(self):
        return self.fecha

@receiver(post_save, sender=SalarioMinimo)
def post_save_salariominimo(sender, instance, **kwargs):
    if kwargs['created']:
        tot_reg = SalarioMinimo.objects.filter(empresa_reg=instance.empresa_reg, vigente=True, active=True).count()
        if tot_reg > 0:
            datos = SalarioMinimo.objects.filter(empresa_reg=instance.empresa_reg, vigente=True, active=True).exclude(pk=instance.pk)
            if datos.count() > 0:
                dato = datos[0]
                dato.vigente = False
                dato.user_mod = instance.user_reg
                dato.date_mod = datetime.datetime.now()
                dato.save()

class Planilla(models.Model):
    correlativo = models.CharField(("Correlativo"), max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=100)
    tipo_planilla = models.ForeignKey("worksheet.TipoNomina", on_delete=models.PROTECT)
    tipo_contrato = models.ForeignKey("worksheet.TipoContrato", verbose_name=("Tipo Contrato"), on_delete=models.PROTECT, blank=True, null=True)
    frecuencia_pago = models.ForeignKey("worksheet.SalaryUnit", on_delete=models.PROTECT)
    fecha_inicio = models.DateField(("Fecha Inicio"), auto_now=False, auto_now_add=False)
    fecha_fin = models.DateField(("Fecha Fin"), auto_now=False, auto_now_add=False)
    fecha_pago = models.DateField(("Fecha Pago"), auto_now=False, auto_now_add=False)
    ihss = models.BooleanField(("Deducir IHSS"), default=False, help_text="Indica si en la planilla a registrar se deducirá IHSS")
    rap = models.BooleanField(("Deducir RAP"), default=False, help_text="Indica si en la planilla a registrar se deducirá RAP")
    imv = models.BooleanField(("Deducir IMV"), default=False, help_text="Indica si en la planilla a registrar se deducirá Impuesto Vecinal")
    isr = models.BooleanField(("Deducir RAP"), default=False, help_text="Indica si en la planilla a registrar se deducirá Impuesto Sobre Renta")
    cerrada = models.BooleanField(("Cerrada"))
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey(Branch, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name='plan_usermod', related_query_name='plan_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField()

    class Meta:
        verbose_name = ("planilla")
        verbose_name_plural = ("planillas")

    def __str__(self):
        return self.descripcion + " - " + str(self.fecha_pago)

class PlanillaDetalle(models.Model):
    planilla = models.ForeignKey("worksheet.Planilla", on_delete=models.PROTECT)
    empleado = models.ForeignKey("worksheet.Employee", on_delete=models.PROTECT)
    salario_diario = models.CharField(max_length=50)
    dias_salario = models.CharField(max_length=50)
    dias_ausentes_sin_pago = models.CharField(max_length=50)
    dias_ausentes_con_pago = models.CharField(max_length=50)
    total_ingresos = models.DecimalField(("Total Ingresos"), max_digits=18, decimal_places=2, blank=True, null=True)
    total_deducciones = models.DecimalField(("Total Deducciones"), max_digits=18, decimal_places=2, blank=True, null=True)
    comentario = models.TextField(("Comentario"))

    empresa_reg = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey(Branch, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name='plandet_usermod', related_query_name='plandet_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField()

    class Meta:
        verbose_name = ("detalle de planilla")
        verbose_name_plural = ("detalles de planillas")

    def __str__(self):
        if self.empleado.middleName:
            return self.planilla.descripcion + " - " + self.empleado.firstName + " " + self.empleado.middleName + " " + self.empleado.lastName
        else:
            return self.planilla.descripcion + " - " + self.empleado.firstName + " " + self.empleado.lastName

class PlanillaDetalleDeducciones(models.Model):
    empleado = models.ForeignKey("worksheet.Employee", verbose_name=("Empleado"), on_delete=models.PROTECT)
    planilla = models.ForeignKey("worksheet.Planilla", verbose_name=("Planilla"), on_delete=models.PROTECT)
    deduccion = models.CharField(("Deduccion"), max_length=250)
    valor = models.DecimalField(("Valor"), max_digits=18, decimal_places=2)
    tipo_deduccion = models.ForeignKey("worksheet.TipoDeduccion", verbose_name=("Tipo Deduccion"), on_delete=models.PROTECT, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey(Branch, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("PlanillaDetalleDeducciones")
        verbose_name_plural = ("PlanillaDetalleDeducciones")

    def __str__(self):
        return self.empleado.firstName + " " + self.empleado.lastName + " | " +  self.planilla.descripcion + " | " + self.deduccion

class PlanillaDetalleIngresos(models.Model):
    empleado = models.ForeignKey("worksheet.Employee", verbose_name=("Empleado"), on_delete=models.PROTECT)
    planilla = models.ForeignKey("worksheet.Planilla", verbose_name=("Planilla"), on_delete=models.PROTECT)
    ingreso = models.CharField(("Ingreso"), max_length=250)
    valor = models.DecimalField(("Valor"), max_digits=18, decimal_places=2)
    tipo_ingreso = models.ForeignKey("worksheet.TipoIngreso", verbose_name=("Tipo Ingreso"), on_delete=models.PROTECT , blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey(Branch, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Planilla Detalle Ingresos")
        verbose_name_plural = ("Planilla Detalle Ingresos")

    def __str__(self):
        return self.empleado.firstName + " " + self.empleado.lastName + " | " +  self.planilla.descripcion + " | " + self.ingreso

class IngresoGeneralDetalle(models.Model):
    ingreso = models.ForeignKey("worksheet.IngresoGeneral", verbose_name=("Ingreso General"), on_delete=models.PROTECT)
    nomina = models.ForeignKey("worksheet.Planilla", verbose_name=("Planilla"), on_delete=models.PROTECT)
    tipo_pago = models.ForeignKey("worksheet.SalaryUnit", verbose_name=("Tipo de Pago"), on_delete=models.PROTECT)
    tipo_contrato = models.ForeignKey("worksheet.TipoContrato", verbose_name=("Tipo de Contrato"), on_delete=models.PROTECT)
    valor = models.DecimalField(("Valor"), max_digits=18, decimal_places=2)
    fecha_valida = models.DateField(("Fecha valida"), auto_now=False, auto_now_add=False)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey("worksheet.Branch", verbose_name=("Sucursal registro"), on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='igd_usermod', related_query_name='igd_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)
    
    class Meta:
        verbose_name = ("Ingreso general detalle")
        verbose_name_plural = ("Ingresos generales detalles")

    def __str__(self):
        return self.ingreso.ingreso_g

class IngresoIndividualDetalle(models.Model):
    empleado = models.ForeignKey("worksheet.Employee", verbose_name=("Empleado"), on_delete=models.PROTECT)
    ingreso = models.ForeignKey("worksheet.IngresoIndividual", verbose_name=("Ingreso"), on_delete=models.PROTECT)
    valor = models.DecimalField(("Valor"), max_digits=18, decimal_places=2)
    fecha_valida = models.DateField(("Fecha valida"), auto_now=False, auto_now_add=False)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey("worksheet.Branch", verbose_name=("Sucursal registro"), on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='iid_usermod', related_query_name='iid_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    class Meta:
        verbose_name = ("Ingreso Individual Detalle")
        verbose_name_plural = ("Ingresos Individuales Detalles")

    def __str__(self):
        return self.ingreso.ingreso_i

class DeduccionGeneralDetalle(models.Model):
    deduccion = models.ForeignKey("worksheet.DeduccionGeneral", verbose_name=("Deduccion General"), on_delete=models.PROTECT)
    nomina = models.ForeignKey("worksheet.Planilla", verbose_name=("Planilla"), on_delete=models.PROTECT)
    tipo_pago = models.ForeignKey("worksheet.SalaryUnit", verbose_name=("Tipo de Pago"), on_delete=models.PROTECT)
    tipo_contrato = models.ForeignKey("worksheet.TipoContrato", verbose_name=("Tipo de Contrato"), on_delete=models.PROTECT)
    valor = models.DecimalField(("Valor"), max_digits=18, decimal_places=2)
    fecha_valido = models.DateField(("Fecha valido"), auto_now=False, auto_now_add=False)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey("worksheet.Branch", verbose_name=("Sucursal registro"), on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='dgd_usermod', related_query_name='dgd_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    class Meta:
        verbose_name = ("Deduccion General Detalle")
        verbose_name_plural = ("Deducciones Generales Detalles")

    def __str__(self):
        return self.deduccion.deduccion_i

class DeduccionIndividualDetalle(models.Model):
    empleado = models.ForeignKey("worksheet.Employee", verbose_name=("Empleado"), on_delete=models.PROTECT)
    deduccion = models.ForeignKey("worksheet.DeduccionIndividual", verbose_name=("Deduccion Individual"), on_delete=models.PROTECT)
    valor = models.DecimalField(("Valor"), max_digits=18, decimal_places=2)
    fecha_valida = models.DateField(("Fecha valida"), auto_now=False, auto_now_add=False)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey("worksheet.Branch", verbose_name=("Sucursal registro"), on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='did_usermod', related_query_name='did_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    class Meta:
        verbose_name = ("Deduccion Individual Detalle")
        verbose_name_plural = ("Deducciones Individuales Detalles")

    def __str__(self):
        return self.empleado.extEmpNo + " - " + self.empleado.firstName + " " + self.empleado.middleName + " " + self.empleado.lastName + " | " + self.deduccion.deduccion_i + " | " + str(self.valor)

class IngresoIndividualPlanilla(models.Model):
    planilla = models.ForeignKey("worksheet.Planilla", verbose_name=("Planilla"), on_delete=models.PROTECT)
    empleado = models.ForeignKey("worksheet.Employee", verbose_name=("Empleado"), on_delete=models.PROTECT)
    ingreso = models.ForeignKey("worksheet.IngresoIndividual", verbose_name=("Ingreso"), on_delete=models.PROTECT)
    valor = models.DecimalField(("Valor"), max_digits=18, decimal_places=2)
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey("worksheet.Branch", verbose_name=("Sucursal registro"), on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, verbose_name=("Usuario registro"), on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='iip_usermod', related_query_name='iip_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(("Activo"))

    class Meta:
        verbose_name = ("ingreso individual planilla")
        verbose_name_plural = ("ingresos individuales planillas")

    def __str__(self):
        return self.planilla.descripcion

class DeduccionIndividualPlanilla(models.Model):
    planilla = models.ForeignKey("worksheet.Planilla", verbose_name=("Planilla"), on_delete=models.PROTECT)
    empleado = models.ForeignKey("worksheet.Employee", verbose_name=("Empleado"), on_delete=models.PROTECT)
    deduccion = models.ForeignKey("worksheet.DeduccionIndividual", verbose_name=("Deduccion"), on_delete=models.PROTECT)
    valor = models.DecimalField(("Valor"), max_digits=18, decimal_places=2)
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    sucursal_reg = models.ForeignKey("worksheet.Branch", verbose_name=("Sucursal registro"), on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, verbose_name=("Usuario registro"), on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='dip_usermod', related_query_name='dip_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(("Activo"))

    class Meta:
        verbose_name = ("DeduccionIndividualPlanilla")
        verbose_name_plural = ("DeduccionesIndividualesPlanillas")

    def __str__(self):
        return self.planilla.descripcion

class DeduccionIndividualSubDetalle(models.Model):
    descripcion = models.TextField(("Descripción"), blank=True, null=True)
    deducciondetalle = models.ForeignKey("worksheet.DeduccionIndividualDetalle", verbose_name=("Detalle Deduccion Individual"), on_delete=models.PROTECT, blank=True, null=True)
    monto = models.DecimalField(("Monto"), max_digits=18, decimal_places=2)
    user_reg = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    active = models.NullBooleanField(default=True)

    class Meta:
        verbose_name = ("deduccionindividualsubdetalle")
        verbose_name_plural = ("deduccionindividualsubdetalles")

    def __str__(self):
        return self.deducciondetalle.empleado.firstName + "|" + self.descripcion + " " + str(self.monto)

    def get_absolute_url(self):
        return reverse("deduccionindividualsubdetalle_detail", kwargs={"pk": self.pk})

class ControlPagosDeduccionIndividual(models.Model):
    planilla = models.ForeignKey("worksheet.Planilla", verbose_name=("Planilla"), on_delete=models.PROTECT)
    deduccion = models.ForeignKey("worksheet.DeduccionIndividualDetalle", verbose_name=("Deducción Individual"), on_delete=models.PROTECT, blank=True, null=True)
    valor = models.DecimalField(("Valor"), max_digits=18, decimal_places=2)

    class Meta:
        verbose_name = ("controlpagosdeduccionindividual")
        verbose_name_plural = ("controlpagosdeduccionindividuales")

    def __str__(self):
        return self.planilla.descripcion + " | " + self.deduccion.deduccion.deduccion_i

    def get_absolute_url(self):
        return reverse("controlpagosdeduccionindividual_detail", kwargs={"pk": self.pk})

class UsuarioCorporacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='uscorp_user', related_query_name='uscorp_user')
    corporacion = models.ForeignKey("worksheet.GrupoCorporativo", verbose_name=("Grupo Corporativo"), on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='uscorp_usermod', related_query_name='uscorp_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)
    
    class Meta:
        verbose_name = ("Usuario Corporacion")
        verbose_name_plural = ("Usuarios Corporaciones")

    def __str__(self):
        return self.usuario.username + " - " + self.corporacion.nombreComercial

class SeguroSocialAjuste(models.Model):
    porcentaje = models.DecimalField(("Porcentaje"), max_digits=9, decimal_places=4)
    maximo_dias = models.CharField(("Maximo Dias"), max_length=50)
    
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, verbose_name=("Usuario registro"), on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='segsocajus_usermod', related_query_name='segsocajus_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(("Activo"))

    class Meta:
        verbose_name = ("segurosocialajuste")
        verbose_name_plural = ("segurosocialajustes")

    def __str__(self):
        return str(self.porcentaje)

class RapDeduccion(models.Model):
    techo = models.CharField(max_length=70)
    porcentaje = models.CharField(max_length=50)

    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='rapded_usermod', related_query_name='rapded_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    class Meta:
        verbose_name = ("Rap Deduccion")
        verbose_name_plural = ("Rap Deducciones")

    def __str__(self):
        return str(self.porcentaje)

class EmpleadoDeducciones(models.Model):
    IHSS = 'IHSS'
    RAP = 'RAP'
    ISR = 'ISR'
    IMV = 'IMV'
    DEDUCCIONES = [
        (IHSS, 'IHSS'),
        (RAP, 'RAP'),
        (ISR, 'Impuesto Sobre Renta'),
        (IMV, 'Impuesto Vecinal'),
    ]
    empleado = models.ForeignKey("worksheet.employee", verbose_name=("Empleado"), on_delete=models.PROTECT)
    deduccion = models.CharField(("Deduccion"), max_length=50, choices=DEDUCCIONES)
    periodo = models.CharField(("Periodo"), max_length=50)
    deduccion_parcial = models.BooleanField(("Deduccion Parcial"), blank=False, null=False)

    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='empded_usermod', related_query_name='empded_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    class Meta:
        verbose_name = ("Asignar Deduccion Legal Empleado")
        verbose_name_plural = ("Asignar Deducciones Legales a Empleado")

    def __str__(self):
        return str(self.empleado.firstName + " " + self.empleado.lastName) + " | " + self.deduccion

class DetallePlanillaDetalleDeduccion(models.Model):
    planilla_detalle_ded = models.OneToOneField("worksheet.PlanillaDetalleDeducciones", verbose_name=("Planilla Detalle Deducción"), on_delete=models.CASCADE)
    deduccion_detalle = models.OneToOneField("worksheet.DeduccionIndividualDetalle", verbose_name=("Deduccion Individual Planilla"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("detalleplanilladetallededuccion")
        verbose_name_plural = ("detalleplanilladetallededucciones")

    def __str__(self):
        return self.planilla_detalle_ded.planilla.descripcion

    def get_absolute_url(self):
        return reverse("detalleplanilladetallededuccion_detail", kwargs={"pk": self.pk})


class LimiteSalarioDeduccion(models.Model):
    salario = models.DecimalField(("Salario"), max_digits=18, decimal_places=4)
    activo = models.BooleanField(("Activo"))
    fecha = models.DateField(("Fecha"), auto_now_add=True)
    empleado = models.ForeignKey("worksheet.Employee", verbose_name=("Empleado"), on_delete=models.PROTECT)
    empresa_reg = models.ForeignKey(Empresa, blank=False, null=False, on_delete=models.PROTECT)
    user_reg = models.ForeignKey(User, blank=False, null=False, on_delete=models.PROTECT)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='limded_usermod', related_query_name='limded_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = ("Limite Salario Deduccion")
        verbose_name_plural = ("Limite Salario Deduccions")

    def __str__(self):
        return self.empleado.firstName + " " +self.empleado.lastName +" | "+ str(self.fecha)