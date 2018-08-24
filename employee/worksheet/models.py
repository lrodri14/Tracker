# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Position(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    active = models.BooleanField(default=True)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='pos_usermod', related_query_name='pos_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='dep_usermod', related_query_name='dep_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='brn_usermod', related_query_name='brn_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='grp_usermod', related_query_name='grp_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class SalesPerson(models.Model):
    slpName = models.CharField(max_length=150)
    groupCode = models.ForeignKey(Group, blank=True, null=True)
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="usermod", related_query_name="usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.slpName

class State(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    name = models.CharField(max_length=150)
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="state_usermod", related_query_name="state_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class Country(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    name = models.CharField(max_length=150)
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="country_usermod", related_query_name="country_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class StatusEmp(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="sts_usermod", related_query_name="sts_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class TermReason(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="trm_usermod", related_query_name="trm_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class Sex(models.Model):
    description = models.CharField(max_length=25)
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="sex_usermod", related_query_name="sex_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.description

class CivilStatus(models.Model):
    description = models.CharField(max_length=50)
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="civStatus_usermod", related_query_name="civStatus_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.description

class SalaryUnit(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="salary_usermod", related_query_name="salary_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class CostUnit(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="cost_usermod", related_query_name="cost_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class Bank(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="bank_usermod", related_query_name="bank_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name



class Employee(models.Model):
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50, blank=True, null=True)
    lastName = models.CharField(max_length=50)
    extEmpNo = models.CharField(max_length=15, blank=True, null=True)
    jobTitle = models.CharField(max_length=50)
    position = models.ForeignKey(Position, help_text="Posición del empleado", verbose_name="Posicion", blank=True, null=True)
    dept = models.ForeignKey(Department, blank=True, null=True)
    branch = models.ForeignKey(Branch, blank=True, null=True)
    slsPerson = models.ForeignKey(SalesPerson, blank=True, null=True)
    officeTel = models.CharField(max_length=50, blank=True, null=True)
    officeExt = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    pager = models.CharField(max_length=50, blank=True, null=True)
    homeTel = models.CharField(max_length=50, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    picture = models.ImageField(upload_to='images/emp_photos')
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

    remark = models.TextField(blank=True, null=True)


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
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='gcom_usermod', related_query_name='gcom_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.nombreComercial

class Empresa(models.Model):
    razonSocial = models.CharField(max_length=100, blank=True, null=True)
    nombreComercial = models.CharField(max_length=100, blank=True, null=True)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='empr_usermod', related_query_name='empr_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.nombreComercial

class Divisiones(models.Model):
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='div_usermod', related_query_name='div_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.descripcion

class CentrosCostos(models.Model):
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='cc_usermod', related_query_name='cc_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.descripcion

class Ciudad(models.Model):
    ID_ciudad = models.CharField(max_length=5, blank=True, null=True)
    nombre = models.CharField(max_length=150)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='cdd_usermod', related_query_name='cdd_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.descripcion

class Parentesco(models.Model):
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='parnt_usermod', related_query_name='parnt_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.descripcion

class FuncionesTrabajo(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='fnT_usermod', related_query_name='fnT_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.nombre

class EquipoTrabajo(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='eqTr_usermod', related_query_name='eqTr_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.nombre

class Ausentismo(models.Model):
    empleado = models.ForeignKey(Employee)
    desde = models.DateField(blank=True, null=True)
    hasta = models.DateField(blank=True, null=True)
    motivo = models.TextField(blank=True, null=True)
    aprobado = models.ForeignKey(Employee, related_name='au_emp', related_query_name='au_emp', blank=True, null=True)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='au_usermod', related_query_name='au_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.empleado.firstName + ' ' + self.empleado.lastName + ' - ' + str(self.desde) + ' | ' + str(self.hasta)

class MotivosAusencia(models.Model):
    descripcion = models.CharField(max_length=150)
    pagado = models.BooleanField()
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='catIng_usermod', related_query_name='catIng_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.descripcion

class MotivosDespido(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='mDes_usermod', related_query_name='mDes_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.nombre

class MotivosRenuncia(models.Model):
    descripcion = models.CharField(max_length=150)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='mRe_usermod', related_query_name='mRe_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.descripcion

class ClaseEducacion(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
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
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='eV_usermod', related_query_name='eV_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)


    def __unicode__(self):
        return self.empleado.firstName + ' ' + self.empleado.lastName + ' | ' + str(self.fecha)


class MotivoAumentoSueldo(models.Model):
    descripcion = models.CharField(max_length=150)
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
    bic_swift = models.CharField(max_length=100, blank=True, null=True)
    of_postal = models.BooleanField()
    cuenta_bancaria = models.CharField(max_length=100)
    sucursal = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.codigo + ' ' + self.nombre + ' ' + self.pais.name

class GrupoComisiones(models.Model):
    descripcion = models.CharField(max_length=150)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='grpcom_usermod', related_query_name='grpcom_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return self.descripcion

class Vendedor(models.Model):
    nombre = models.CharField(max_length=150)
    grupo_comisiones = models.ForeignKey(GrupoComisiones)
    porcentaje_comision = models.CharField(max_length=15, blank=True, null=True)
    empleado = models.ForeignKey(Employee)
    telefono = models.CharField(max_length=25, blank=True, null=True)
    tel_movil = models.CharField(max_length=25)
    correo = models.CharField(max_length=150)
    comentario = models.TextField(blank=True, null=True)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='vendedor_usermod', related_query_name='vendedor_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.nombre

class Feriado(models.Model):
    fecha = models.DateField()
    rate = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=150)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='fer_usermod', related_query_name='fer_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return str(self.fecha)

class ActivoAsignado(models.Model):
    descripcion = models.CharField(max_length=150)
    user_reg = models.ForeignKey(User)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='actasig_usermod', related_query_name='actasig_usermod')
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return self.descripcion
    