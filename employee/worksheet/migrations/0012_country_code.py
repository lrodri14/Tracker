# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-15 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0011_centroscostos'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]