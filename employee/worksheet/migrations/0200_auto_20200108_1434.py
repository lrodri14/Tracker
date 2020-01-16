# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-01-08 20:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0199_detalleplanilladetallededuccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleplanilladetallededuccion',
            name='deduccion_detalle',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='worksheet.DeduccionIndividualDetalle', verbose_name='Deduccion Individual Planilla'),
        ),
        migrations.AlterField(
            model_name='detalleplanilladetallededuccion',
            name='planilla_detalle_ded',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='worksheet.PlanillaDetalleDeducciones', verbose_name='Planilla Detalle Deducción'),
        ),
    ]
