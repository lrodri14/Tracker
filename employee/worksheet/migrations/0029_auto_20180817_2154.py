# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-18 03:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worksheet', '0028_evaluacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacion',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='date_reg',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='user_mod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eV_usermod', related_query_name='eV_usermod', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='user_reg',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
