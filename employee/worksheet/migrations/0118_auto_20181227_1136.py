# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-27 17:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0117_auto_20181227_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incrementossalariales',
            name='empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='worksheet.Employee', verbose_name='Empleado'),
        ),
    ]
