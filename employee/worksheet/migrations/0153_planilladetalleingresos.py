# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-30 22:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worksheet', '0152_auto_20190330_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanillaDetalleIngresos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingreso', models.CharField(max_length=250, verbose_name='Deduccion')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='Valor')),
                ('date_reg', models.DateTimeField(auto_now_add=True)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Employee', verbose_name='Empleado')),
                ('empresa_reg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Empresa')),
                ('planilla', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Planilla', verbose_name='Planilla')),
                ('sucursal_reg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Branch')),
                ('user_reg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'PlanillaDetalleIngresos',
                'verbose_name_plural': 'PlanillaDetalleIngresos',
            },
        ),
    ]