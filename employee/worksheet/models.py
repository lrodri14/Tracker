# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name='grp_usermod', related_query_name='grp_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class Empresa(models.Model):
    razonSocial = models.CharField(max_length=100, blank=True, null=True)
    nombreComercial = models.CharField(max_length=100, blank=True, null=True)
    grupo = models.ForeignKey(Group, blank=True, null=True)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='empr_usermod', related_query_name='empr_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.nombreComercial

class Branch(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    description = models.CharField(max_length=250)
    empresa = models.ForeignKey(Empresa)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='brn_usermod', related_query_name='brn_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)


    def __unicode__(self):
        return self.description

class Position(models.Model):
    code = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=250)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="pos_empreg", related_query_name="pos_empreg")
    active = models.BooleanField(default=True)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='pos_usermod', related_query_name='pos_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        return self.description

class Department(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    description = models.CharField(max_length=250)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="dep_empreg", related_query_name="dep_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='dep_usermod', related_query_name='dep_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.description	

class SalesPerson(models.Model):
    slpName = models.CharField(max_length=150)
    groupCode = models.ForeignKey(Group, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="slsp_empreg", related_query_name="slsp_empreg")
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="usermod", related_query_name="usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
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

    def __unicode__(self):
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

    def __unicode__(self):
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

    def __unicode__(self):
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

    def __unicode__(self):
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

    def __unicode__(self):
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

    def __unicode__(self):
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

    def __unicode__(self):
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

    def __unicode__(self):
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

    def __unicode__(self):
        return self.description

class GrupoComisiones(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=150)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING,
                                    related_name="gpCom_empreg", related_query_name="gpCom_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name='grpcom_usermod', related_query_name='grpcom_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return self.descripcion

class Vendedor(models.Model):
    nombre = models.CharField(max_length=150)
    grupo_comisiones = models.ForeignKey(GrupoComisiones)
    porcentaje_comision = models.CharField(
        max_length=15, blank=True, null=True)
    telefono = models.CharField(max_length=25, blank=True, null=True)
    tel_movil = models.CharField(max_length=25)
    correo = models.CharField(max_length=150)
    comentario = models.TextField(blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING,
                                    related_name="vendedor_empreg", related_query_name="vendedor_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name='vendedor_usermod', related_query_name='vendedor_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.nombre


class TipoNomina(models.Model):
    tipo_planilla = models.CharField(max_length=100)
    descripcion = models.TextField()
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name='tnom_usermod', related_query_name='tnom_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return self.tipo_planilla


class TipoContrato(models.Model):
    tipo_contrato = models.CharField(max_length=100)
    descripcion = models.TextField()
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name='tcon_usermod', related_query_name='tcon_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return self.tipo_contrato

class Employee(models.Model):
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50, blank=True, null=True)
    lastName = models.CharField(max_length=50)
    extEmpNo = models.CharField(max_length=15, blank=True, null=True)
    jobTitle = models.CharField(max_length=50)
    position = models.ForeignKey(Position, help_text="Posición del empleado", verbose_name="Posicion", blank=True, null=True)
    dept = models.ForeignKey(Department, blank=True, null=True)
    branch = models.ForeignKey(Branch, blank=True, null=True)
    jefe = models.ForeignKey('self', blank=True, null=True)
    slsPerson = models.ForeignKey(Vendedor, blank=True, null=True)
    officeTel = models.CharField(max_length=50, blank=True, null=True)
    officeExt = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    pager = models.CharField(max_length=50, blank=True, null=True)
    homeTel = models.CharField(max_length=50, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
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
    status = models.ForeignKey(StatusEmp, blank=True, null=True)
    termDate = models.DateField(blank=True, null=True)
    termReason = models.ForeignKey(TermReason, blank=True, null=True)

    sex = models.ForeignKey(Sex, blank=True, null=True)
    birthDate = models.DateField(blank=True, null=True)
    birthCountry = models.ForeignKey(Country, blank=True, null=True)
    marrStatus = models.ForeignKey(CivilStatus, blank=True, null=True)
    nChildren = models.CharField(max_length=12 ,blank=True, null=True)
    govID = models.CharField(max_length=50, blank=True, null=True)
    citizenship = models.ForeignKey(Country, blank=True, null=True, related_name='citizenship', related_query_name='citizenship')
    passportNo = models.CharField(max_length=50, blank=True, null=True)
    passportExt = models.DateField(blank=True, null=True)
    passIssue = models.DateField(blank=True, null=True)
    passIssuer = models.CharField(max_length=150, blank=True, null=True)

    salary = models.CharField(max_length=20, blank=True, null=True)
    salaryUnits = models.ForeignKey(SalaryUnit, blank=True, null=True)
    empCost = models.CharField(max_length=20, blank=True, null=True)
    empCostUnit = models.ForeignKey(CostUnit, blank=True, null=True)
    bankCode = models.ForeignKey(Bank, blank=True, null=True)
    bankAccount = models.CharField(max_length=50, blank=True, null=True)
    branchBank = models.CharField(max_length=150, blank=True, null=True)
    tipo_nomina = models.ForeignKey("worksheet.TipoNomina", verbose_name="tipo nomina", on_delete=models.PROTECT, blank=True, null=True)
    tipo_contrato = models.ForeignKey("worksheet.TipoContrato", verbose_name="tipo contrato", on_delete=models.PROTECT, blank=True, null=True)

    remark = models.TextField(blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="empl_empreg", related_query_name="empl_empreg")


    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='emp_usermod', related_query_name='emp_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.firstName + ' ' + self.lastName

class GrupoCorporativo(models.Model):
    razonSocial = models.CharField(max_length=100, blank=True, null=True)
    nombreComercial = models.CharField(max_length=100, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="group_empreg", related_query_name="group_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='gcom_usermod', related_query_name='gcom_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.nombreComercial

class Divisiones(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="div_empreg", related_query_name="div_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='div_usermod', related_query_name='div_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.descripcion

class CentrosCostos(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="cc_empreg", related_query_name="cc_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='cc_usermod', related_query_name='cc_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.descripcion

class Ciudad(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    nombre = models.CharField(max_length=150)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="ciudad_empreg", related_query_name="ciudad_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='cdd_usermod', related_query_name='cdd_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.nombre

class Parentesco(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="parent_empreg", related_query_name="parent_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='parnt_usermod', related_query_name='parnt_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.descripcion

class FuncionesTrabajo(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="fun_empreg", related_query_name="fun_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='fnT_usermod', related_query_name='fnT_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.nombre

class EquipoTrabajo(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="eqtr_empreg", related_query_name="eqtr_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='eqTr_usermod', related_query_name='eqTr_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.nombre

class MotivosAusencia(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=150)
    pagado = models.BooleanField()
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="motIng_empreg", related_query_name="motIng_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='catIng_usermod', related_query_name='catIng_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.descripcion

class Ausentismo(models.Model):
    empleado = models.ForeignKey(Employee)
    desde = models.DateField(blank=True, null=True)
    hasta = models.DateField(blank=True, null=True)
    motivo = models.ForeignKey(MotivosAusencia, blank=True, null=True, on_delete=models.DO_NOTHING)
    aprobado = models.ForeignKey(Employee, related_name='au_emp', related_query_name='au_emp', blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="au_empreg", related_query_name="au_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='au_usermod', related_query_name='au_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.empleado.firstName + ' ' + self.empleado.lastName + ' - ' + str(self.desde) + ' | ' + str(self.hasta)

class MotivosDespido(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="mDes_empreg", related_query_name="mDes_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='mDes_usermod', related_query_name='mDes_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.nombre

class MotivosRenuncia(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=150)
    user_reg = models.ForeignKey(User)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="mRe_empreg", related_query_name="mRe_empreg")
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='mRe_usermod', related_query_name='mRe_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.descripcion

class ClaseEducacion(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="clsEd_empreg", related_query_name="clsEd_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='clsEdu_usermod', related_query_name='clsEdu_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.nombre

class Educacion(models.Model):
    empleado = models.ForeignKey(Employee)
    desde = models.DateField()
    hasta = models.DateField()
    clase_edu = models.ForeignKey(ClaseEducacion, blank=True, null=True, on_delete=models.SET_NULL)
    entidad = models.CharField(max_length=100, blank=True, null=True)
    asignatura_principal = models.CharField(max_length=100, blank=True, null=True)
    titulo = models.CharField(max_length=100, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="Ed_empreg", related_query_name="Ed_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='edu_usermod', related_query_name='edu_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.empleado.firstName + ' ' + self.empleado.lastName + ' | ' + self.clase_edu.nombre

class Evaluacion(models.Model):
    empleado = models.ForeignKey(Employee)
    fecha = models.DateField()
    descripcion = models.TextField()
    gerente = models.ForeignKey(Employee,  blank=True, null=True, on_delete=models.SET_NULL, related_name='eV_gerente', related_query_name="eV_gerente")
    grupo_salarial = models.CharField(max_length=100)
    comentario = models.TextField()
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="eV_empreg", related_query_name="eV_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='eV_usermod', related_query_name='eV_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)


    def __unicode__(self):
        return self.empleado.firstName + ' ' + self.empleado.lastName + ' | ' + str(self.fecha)

class MotivoAumentoSueldo(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=150)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="mAuSal_empreg", related_query_name="mAuSal_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name='mAuSal_usermod', related_query_name='mAuSal_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.descripcion

class EmpleosAnteriores(models.Model):
    empleado = models.ForeignKey(Employee)
    desde = models.DateField()
    hasta = models.DateField()
    empresa = models.CharField(max_length=100, blank=True, null=True)
    posicion = models.CharField(max_length=100, blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="empAnt_empreg", related_query_name="empAnt_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='empAnt_usermod', related_query_name='empAnt_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.empleado.firstName

class Banco(models.Model):
    pais = models.ForeignKey(Country)
    codigo = models.CharField(max_length=15)
    nombre = models.CharField(max_length=100)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="Banco_empreg", related_query_name="Banco_empreg")
    bic_swift = models.CharField(max_length=100, blank=True, null=True)
    of_postal = models.BooleanField()
    cuenta_bancaria = models.CharField(max_length=100)
    sucursal = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.codigo + ' ' + self.nombre + ' ' + self.pais.name

class Feriado(models.Model):
    fecha = models.DateField()
    rate = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=150)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="feriado_empreg", related_query_name="feriado_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='fer_usermod', related_query_name='fer_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return str(self.fecha)

class ActivoAsignado(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    descripcion = models.CharField(max_length=150)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="actasig_empreg", related_query_name="actasig_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='actasig_usermod', related_query_name='actasig_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return self.descripcion
    
class UsuarioEmpresa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='usemp_user', related_query_name='usemp_user')
    empresa = models.ForeignKey(Empresa)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="usemp_empreg", related_query_name="usemp_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='usemp_usermod', related_query_name='usemp_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return self.usuario.username + " - " + self.empresa.nombreComercial

class UsuarioSucursal(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='usbranch_user', related_query_name='usbranch_user')
    sucursal = models.ForeignKey(Branch, blank=True, null=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="usbranch_empreg", related_query_name="usbranch_empreg")
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='usbranc_usermod', related_query_name='usbranch_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return self.usuario.username + " - " + self.sucursal.description

class ImagenEmpleado(models.Model):
    empleado = models.OneToOneField("worksheet.employee", verbose_name="Empleado", on_delete=models.DO_NOTHING)
    imagen = models.ImageField(upload_to='images/emp_photos')
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="imgemp_empreg", related_query_name="imgemp_empreg")
    user_reg = models.ForeignKey(User, blank=True, null=True)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='imgemp_usermod', related_query_name='imgemp_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)
    
    def __unicode__(self):
        return self.empleado.firstName + " " + self.empleado.lastName

class TipoIngreso(models.Model):
    tipo_ingreso = models.CharField(max_length=50)
    descripcion = models.TextField()
    empresa_reg = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='ting_usermod', related_query_name='ting_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return self.tipo_ingreso


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

    def __unicode__(self):
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

    def __unicode__(self):
        return self.ingreso_g


#Transacciones
class IncrementosSalariales(models.Model):
    empleado = models.ForeignKey("worksheet.employee", verbose_name="Empleado", on_delete=models.DO_NOTHING)
    fecha_incremento = models.DateField()
    motivo_aumento = models.ForeignKey(MotivoAumentoSueldo, on_delete=models.DO_NOTHING)
    salario_anterior = models.DecimalField(max_digits=18, decimal_places=3)
    incremento = models.DecimalField(max_digits=18, decimal_places=3)
    nuevo_salario = models.DecimalField(max_digits=18, decimal_places=3)
    comentarios = models.TextField(blank=True, null=True)
    salario_actual = models.BooleanField(blank=False, null=False, default=True)
    empresa_reg = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING)
    user_reg = models.ForeignKey(User, blank=True, null=True)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='incsal_usermod', related_query_name='incsal_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
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
                
                print "Actualizo empleado"
        d_empleado = Employee.objects.get(pk=instance.empleado.pk)
        d_empleado.salary = str(instance.nuevo_salario)
        d_empleado.save()
