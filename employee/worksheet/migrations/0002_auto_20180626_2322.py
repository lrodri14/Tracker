# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-27 05:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='middleName',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
