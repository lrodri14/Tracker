# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-26 16:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0042_auto_20180823_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ausentismo',
            name='motivo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='worksheet.MotivosAusencia'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='empCost',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='salary',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]