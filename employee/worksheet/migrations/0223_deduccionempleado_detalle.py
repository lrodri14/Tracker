# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-10-05 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0222_deduccionindividualsubdetalle_deduccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduccionempleado',
            name='detalle',
            field=models.BooleanField(default=False, verbose_name='Requiere detalle'),
        ),
    ]