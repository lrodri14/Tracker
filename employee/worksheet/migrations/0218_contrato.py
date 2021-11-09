# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-09-08 17:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worksheet', '0217_ausentismo_fecha_aplica'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=250, verbose_name='Numero contrato')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha Inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha Fin')),
                ('date_reg', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('date_mod', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Employee', verbose_name='Empleado')),
                ('empresa_reg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Empresa')),
                ('tipo_contrato', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.TipoContrato', verbose_name='Tipo de Contrato')),
                ('user_mod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cont_usermod', related_query_name='cont_usermod', to=settings.AUTH_USER_MODEL)),
                ('user_reg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cont_userreg', related_query_name='cont_userreg', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'contrato',
                'verbose_name_plural': 'contratos',
            },
        ),
    ]
