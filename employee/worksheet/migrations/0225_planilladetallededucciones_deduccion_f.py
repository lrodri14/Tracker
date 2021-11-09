# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-10-19 17:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0224_deduccionindividualsubdetalle_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='planilladetallededucciones',
            name='deduccion_f',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='worksheet.DeduccionEmpleado', verbose_name='Deduccion empleado'),
        ),
    ]
