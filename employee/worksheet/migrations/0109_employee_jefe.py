# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-29 19:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0108_employee_slsperson'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='jefe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='worksheet.Employee'),
        ),
    ]
