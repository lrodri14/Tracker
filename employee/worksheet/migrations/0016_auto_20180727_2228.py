# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-28 04:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0015_auto_20180727_2201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sex',
            name='name',
        ),
        migrations.AlterField(
            model_name='sex',
            name='description',
            field=models.CharField(max_length=25),
        ),
    ]
