# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-02 05:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0021_ausentismo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ausentismo',
            name='aprobado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='au_emp', related_query_name='au_emp', to='worksheet.Employee'),
        ),
        migrations.AlterField(
            model_name='ausentismo',
            name='desde',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ausentismo',
            name='hasta',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ausentismo',
            name='motivo',
            field=models.TextField(blank=True, null=True),
        ),
    ]