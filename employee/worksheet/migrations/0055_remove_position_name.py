# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-20 17:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0054_state_empresa_reg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='name',
        ),
    ]
