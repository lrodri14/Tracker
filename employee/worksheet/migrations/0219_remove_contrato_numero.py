# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-09-09 21:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0218_contrato'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contrato',
            name='numero',
        ),
    ]