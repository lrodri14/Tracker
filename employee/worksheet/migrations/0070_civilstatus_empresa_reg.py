# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-21 19:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0069_remove_sex_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='civilstatus',
            name='empresa_reg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cvlstatus_empreg', related_query_name='cvlstatus_empreg', to='worksheet.Empresa'),
        ),
    ]
