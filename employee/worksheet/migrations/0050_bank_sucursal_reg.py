# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-05 07:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0049_usuariosucursal'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='sucursal_reg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bank_sucreg', related_query_name='bank_sucreg', to='worksheet.Branch'),
        ),
    ]
