# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-23 14:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0038_activoasignado'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmpleoAnterior',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desde', models.DateField()),
                ('hasta', models.DateField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worksheet.Employee')),
            ],
        ),
    ]
