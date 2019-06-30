# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-28 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0165_auto_20190627_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='socialNetwork1',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Red Social 1'),
        ),
        migrations.AddField(
            model_name='employee',
            name='socialNetwork2',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Red Social 2'),
        ),
    ]
