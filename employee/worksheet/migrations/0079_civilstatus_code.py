# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-22 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0078_sex_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='civilstatus',
            name='code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]