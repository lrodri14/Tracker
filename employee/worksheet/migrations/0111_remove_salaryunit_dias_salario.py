# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-04 14:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0110_salaryunit_dias_salario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salaryunit',
            name='dias_salario',
        ),
    ]
