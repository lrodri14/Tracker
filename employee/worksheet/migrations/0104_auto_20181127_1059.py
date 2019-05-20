# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-27 16:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worksheet', '0103_auto_20181126_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='pais',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='state_pais', related_query_name='state_pais', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usuarioempresa',
            name='empresa_reg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='usemp_empreg', related_query_name='usemp_empreg', to='worksheet.Empresa'),
        ),
        migrations.AddField(
            model_name='usuariosucursal',
            name='empresa_reg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='usbranch_empreg', related_query_name='usbranch_empreg', to='worksheet.Empresa'),
        ),
    ]
