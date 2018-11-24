# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-23 21:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0090_equipotrabajo_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='motivosausencia',
            name='code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='motivosausencia',
            name='empresa_reg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='motIng_empreg', related_query_name='motIng_empreg', to='worksheet.Empresa'),
        ),
    ]
