# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-21 14:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0059_country_empresa_reg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='name',
        ),
    ]
