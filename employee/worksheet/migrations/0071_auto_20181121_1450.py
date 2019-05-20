# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-21 20:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0070_civilstatus_empresa_reg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salaryunit',
            name='name',
        ),
        migrations.AddField(
            model_name='salaryunit',
            name='empresa_reg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='slrunt_empreg', related_query_name='slrunt_empreg', to='worksheet.Empresa'),
        ),
    ]
