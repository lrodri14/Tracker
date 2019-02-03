# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-30 19:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worksheet', '0126_planilla_correlativo'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanillaDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salario_diario', models.CharField(max_length=50)),
                ('dias_salario', models.CharField(max_length=50)),
                ('date_reg', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(blank=True, null=True)),
                ('active', models.NullBooleanField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Employee')),
                ('empresa_reg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Empresa')),
                ('planilla', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Planilla')),
                ('sucursal_reg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Branch')),
                ('user_mod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='plandet_usermod', related_query_name='plandet_usermod', to=settings.AUTH_USER_MODEL)),
                ('user_reg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'detalle de planilla',
                'verbose_name_plural': 'detalles de planillas',
            },
        ),
    ]