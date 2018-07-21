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
    name = models.CharField(max_length=25)
    description = models.TextField()
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="sex_usermod", related_query_name="sex_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class CivilStatus(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    user_reg = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_reg = models.DateTimeField(auto_now_add=True)
    user_mod = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="civStatus_usermod", related_query_name="civStatus_usermod",)
    date_mod = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

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
    extEmpNo = models.CharField(max_length=15)
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
    nChildren = models.IntegerField(blank=True, null=True)
    govID = models.CharField(max_length=50, blank=True, null=True)
    citizenship = models.ForeignKey(Country, blank=True, null=True, related_name='citizenship', related_query_name='citizenship')
    passportNo = models.CharField(max_length=50, blank=True, null=True)
    passportExt = models.DateField(blank=True, null=True)
    passIssue = models.DateField(blank=True, null=True)
    passIssuer = models.CharField(max_length=150, blank=True, null=True)

    salary = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)
    salaryUnits = models.ForeignKey(SalaryUnit, blank=True, null=True)
    empCost = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)
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
