# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-31 12:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0015_auto_20180109_1822'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tarjeton',
            old_name='Esquema_de_pago',
            new_name='esquema_de_pago',
        ),
        migrations.AddField(
            model_name='pagosalumno',
            name='concepto',
            field=models.CharField(choices=[('Inscripcion', 'Inscripcion'), ('Colegiatura', 'Colegiatura')], default='Colegiatura', max_length=20),
        ),
        migrations.AddField(
            model_name='pagosalumno',
            name='movimiento_verificado_por_direccion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tarjeton',
            name='pagos_atrasados',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tarjeton',
            name='proxima_fecha_de_pago',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pagosalumno',
            name='forma_de_pago',
            field=models.CharField(choices=[('Efectivo', 'Efectivo'), ('Deposito', 'Deposito'), ('Transferencia', 'Transferencia'), ('Cheque', 'Cheque'), ('Otro', 'Otro')], default='Efectivo', max_length=20),
        ),
        migrations.AlterField(
            model_name='tarjeton',
            name='descripcion',
            field=models.CharField(default='Creacion: <function now at 0x7f162a1067b8>', help_text='Descripcion breve relativa al tarjeton', max_length=100),
        ),
    ]
