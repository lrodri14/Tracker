# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-29 16:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worksheet', '0157_planilladetalle_comentario'),
    ]

    operations = [
        migrations.CreateModel(
            name='RapDeduccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('techo', models.CharField(max_length=70)),
                ('porcentaje', models.CharField(max_length=50)),
                ('date_reg', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(blank=True, null=True)),
                ('active', models.NullBooleanField()),
                ('empresa_reg', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='worksheet.Empresa')),
                ('user_mod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rapded_usermod', related_query_name='rapded_usermod', to=settings.AUTH_USER_MODEL)),
                ('user_reg', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Rap Deduccion',
                'verbose_name_plural': 'Rap Deducciones',
            },
        ),
    ]
