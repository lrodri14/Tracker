# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-22 23:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0080_employee_empresa_reg'),
    ]

    operations = [
        migrations.AddField(
            model_name='divisiones',
            name='code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]