# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-28 21:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0106_remove_vendedor_empleado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='slsPerson',
        ),
    ]