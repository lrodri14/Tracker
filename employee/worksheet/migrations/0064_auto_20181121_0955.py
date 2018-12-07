# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-21 15:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0063_statusemp_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ciudad',
            name='ID_ciudad',
        ),
        migrations.AddField(
            model_name='ciudad',
            name='empresa_reg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ciudad_empreg', related_query_name='ciudad_empreg', to='worksheet.Empresa'),
        ),
    ]