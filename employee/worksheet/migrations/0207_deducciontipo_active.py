# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-08-14 19:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheet', '0206_auto_20200812_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='deducciontipo',
            name='active',
            field=models.BooleanField(default=1, verbose_name='Activo'),
            preserve_default=False,
        ),
    ]
