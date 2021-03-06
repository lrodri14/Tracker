# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-21 17:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0067_termreason_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='sex',
            name='code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='sex',
            name='empresa_reg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sex_empreg', related_query_name='sex_empreg', to='worksheet.Empresa'),
        ),
    ]
