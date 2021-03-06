# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-11 22:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worksheet', '0139_auto_20190307_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngresoIndividualDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='Valor')),
                ('fecha_valida', models.DateField(verbose_name='Fecha valida')),
                ('date_reg', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(blank=True, null=True)),
                ('active', models.NullBooleanField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Employee', verbose_name='Empleado')),
                ('empresa_reg', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='worksheet.Empresa')),
                ('ingreso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.IngresoIndividual', verbose_name='Ingreso')),
                ('sucursal_reg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Branch', verbose_name='Sucursal registro')),
                ('user_mod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='iid_usermod', related_query_name='iid_usermod', to=settings.AUTH_USER_MODEL)),
                ('user_reg', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ingreso Individual Detalle',
                'verbose_name_plural': 'Ingresos Individuales Detalles',
            },
        ),
        migrations.AlterModelOptions(
            name='ingresogeneraldetalle',
            options={'verbose_name': 'Ingreso general detalle', 'verbose_name_plural': 'Ingresos generales detalles'},
        ),
    ]
