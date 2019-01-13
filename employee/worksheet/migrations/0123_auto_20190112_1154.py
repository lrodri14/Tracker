# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-01-12 17:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0122_auto_20190112_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='tipo_contrato',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='worksheet.TipoContrato', verbose_name='tipo contrato'),
        ),
        migrations.AddField(
            model_name='employee',
            name='tipo_nomina',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='worksheet.TipoNomina', verbose_name='tipo nomina'),
        ),
    ]
