# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-08-24 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0210_auto_20200822_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduccionempleado',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Activo'),
        ),
    ]
