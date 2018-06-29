# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from worksheet.models import *

# Register your models here.
admin.site.register(Position)
admin.site.register(Department)
admin.site.register(Group)
admin.site.register(Branch)
admin.site.register(SalesPerson)
admin.site.register(Employee)
admin.site.register(State)
admin.site.register(Country)