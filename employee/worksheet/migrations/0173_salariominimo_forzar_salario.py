# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-08 20:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0172_planilla_tipo_contrato'),
    ]

    operations = [
        migrations.AddField(
            model_name='salariominimo',
            name='forzar_salario',
            field=models.NullBooleanField(verbose_name='Forzar salario'),
        ),
    ]
