# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-13 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0189_tipoingreso_grupo'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipodeduccion',
            name='grupo',
            field=models.CharField(blank=True, choices=[('IHSS', 'IHSS'), ('IMV', 'IMPUESTO VECINAL'), ('ISR', 'ISR'), ('RAP', 'RAP'), ('OTRAS_DEDUCCIONES', 'OTRAS DEDUCCIONES')], max_length=20, null=True, verbose_name='Grupo'),
        ),
    ]
