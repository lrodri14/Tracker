# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-20 19:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0032_banco_grupocomisiones_vendedor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grupocomisiones',
            name='active',
        ),
        migrations.RemoveField(
            model_name='grupocomisiones',
            name='date_mod',
        ),
    ]
