# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-21 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0035_grupocomisiones_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendedor',
            name='porcentaje_comision',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
