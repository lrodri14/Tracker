# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-09-03 22:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0213_auto_20200828_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planilladetallededucciones',
            name='tipo_deduccion',
        ),
        migrations.RemoveField(
            model_name='planilladetalleingresos',
            name='tipo_ingreso',
        ),
    ]
