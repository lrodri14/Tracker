# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-26 19:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0100_auto_20181126_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendedor',
            name='empresa_reg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='vendedor_empreg', related_query_name='vendedor_empreg', to='worksheet.Empresa'),
        ),
    ]
