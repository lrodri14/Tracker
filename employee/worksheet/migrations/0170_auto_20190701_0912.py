# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-01 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0169_employee_metodo_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='metodo_pago',
            field=models.IntegerField(blank=True, null=True, verbose_name='Metodo de Pago'),
        ),
    ]