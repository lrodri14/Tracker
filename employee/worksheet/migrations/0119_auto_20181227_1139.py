# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-27 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0118_auto_20181227_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incrementossalariales',
            name='salario_actual',
            field=models.BooleanField(),
        ),
    ]