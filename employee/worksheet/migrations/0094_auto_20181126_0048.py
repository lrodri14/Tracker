# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-26 06:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0093_auto_20181125_2326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claseeducacion',
            name='nombre',
        ),
        migrations.AddField(
            model_name='claseeducacion',
            name='code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='claseeducacion',
            name='empresa_reg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='clsEd_empreg', related_query_name='clsEd_empreg', to='worksheet.Empresa'),
        ),
        migrations.AddField(
            model_name='motivosrenuncia',
            name='code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='motivosrenuncia',
            name='empresa_reg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='mRe_empreg', related_query_name='mRe_empreg', to='worksheet.Empresa'),
        ),
    ]