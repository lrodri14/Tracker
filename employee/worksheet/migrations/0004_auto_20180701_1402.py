# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-01 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0003_auto_20180627_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='active',
            field=models.BooleanField(),
        ),
    ]
