# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-20 17:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0055_remove_position_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
