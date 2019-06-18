# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-11 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0160_auto_20190603_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleadodeducciones',
            name='deduccion_parcial',
            field=models.BooleanField(default=1, verbose_name='Deduccion Parcial'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empleadodeducciones',
            name='periodo',
            field=models.CharField(default=True, max_length=50, verbose_name='Periodo'),
            preserve_default=False,
        ),
    ]
