# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-22 15:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0076_auto_20181122_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='bank',
            name='empresa_reg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bank_empreg', related_query_name='bank_empreg', to='worksheet.Empresa'),
        ),
    ]