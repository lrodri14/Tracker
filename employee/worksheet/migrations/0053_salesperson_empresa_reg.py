# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-19 22:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0052_department_empresa_reg'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesperson',
            name='empresa_reg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='slsp_empreg', related_query_name='slsp_empreg', to='worksheet.Empresa'),
        ),
    ]
