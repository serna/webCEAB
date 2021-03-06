# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-06 11:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0025_egresogenerales_plantel'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarjeton',
            name='fecha_abonos_anticipados',
            field=models.DateField(default=django.utils.timezone.now, help_text='Solo se tomaran en cuenta los pagos que se hayan hecho desde esta fecha'),
        ),
        migrations.AlterField(
            model_name='tarjeton',
            name='inicio',
            field=models.DateField(default=django.utils.timezone.now, help_text='Fecha del primer pago programado, esta fecha sirve para agendar los pagos siguientes'),
        ),
    ]
