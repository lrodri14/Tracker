# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-15 19:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worksheet', '0010_divisiones'),
    ]

    operations = [
        migrations.CreateModel(
            name='CentrosCostos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(blank=True, max_length=250, null=True)),
                ('date_reg', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField()),
                ('user_mod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cc_usermod', related_query_name='cc_usermod', to=settings.AUTH_USER_MODEL)),
                ('user_reg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
