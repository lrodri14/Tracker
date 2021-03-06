# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-21 19:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worksheet', '0036_auto_20180821_1303'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feriado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('rate', models.CharField(max_length=10)),
                ('descripcion', models.CharField(max_length=150)),
                ('date_reg', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField()),
                ('user_mod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fer_usermod', related_query_name='fer_usermod', to=settings.AUTH_USER_MODEL)),
                ('user_reg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
