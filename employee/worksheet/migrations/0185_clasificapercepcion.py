# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-06 17:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worksheet', '0184_encabezadoimpuestosobrerenta_valor'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClasificaPercepcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupo', models.CharField(choices=[('BONO', 'BONOS'), ('OTROS', 'OTROS INGRESOS')], max_length=20, verbose_name='Grupo')),
                ('date_reg', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField()),
                ('empresa_reg', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='worksheet.Empresa')),
                ('tipo_ingreso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.TipoIngreso', verbose_name='Tipo Ingreso')),
                ('user_mod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='claPer_usermod', related_query_name='claPer_usermod', to=settings.AUTH_USER_MODEL)),
                ('user_reg', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Clasifica Percepcion',
                'verbose_name_plural': 'Clasifica Percepciones',
            },
        ),
    ]
