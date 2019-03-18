# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-16 18:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0143_ingresoindividualplanilla'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingresoindividualplanilla',
            name='active',
            field=models.BooleanField(verbose_name='Activo'),
        ),
        migrations.AlterField(
            model_name='ingresoindividualplanilla',
            name='empresa_reg',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Empresa'),
        ),
    ]