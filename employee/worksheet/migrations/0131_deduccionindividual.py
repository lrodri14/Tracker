# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-02-21 16:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worksheet', '0130_tipodeduccion'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeduccionIndividual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deduccion_i', models.CharField(max_length=50)),
                ('control_saldo', models.BooleanField(default=True)),
                ('date_reg', models.DateTimeField(auto_now_add=True)),
                ('date_mod', models.DateTimeField(blank=True, null=True)),
                ('active', models.NullBooleanField()),
                ('empresa_reg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Empresa')),
                ('sucursal_reg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.Branch')),
                ('tipo_deduccion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='worksheet.TipoDeduccion', verbose_name='deduccion individual')),
                ('user_mod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dedind_usermod', related_query_name='dedind_usermod', to=settings.AUTH_USER_MODEL)),
                ('user_reg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Deduccion Individual',
                'verbose_name_plural': 'Deducciones Individuales',
            },
        ),
    ]
