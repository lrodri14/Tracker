# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-21 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0064_auto_20181121_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciudad',
            name='code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
