# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-09-07 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0216_auto_20200904_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='ausentismo',
            name='fecha_aplica',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha aplica'),
        ),
    ]
