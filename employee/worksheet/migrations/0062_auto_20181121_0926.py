# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-21 15:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0061_branch_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statusemp',
            name='name',
        ),
        migrations.AddField(
            model_name='statusemp',
            name='empresa_reg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='stemp_empreg', related_query_name='stemp_empreg', to='worksheet.Empresa'),
        ),
    ]
