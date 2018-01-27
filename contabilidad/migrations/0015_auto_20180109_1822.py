# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-10 00:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0014_auto_20180106_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarjeton',
            name='descripcion',
            field=models.CharField(default='Creacion: <function now at 0x7f4dc56047b8>', help_text='Descripcion breve relativa al tarjeton', max_length=100),
        ),
        migrations.AddField(
            model_name='tarjeton',
            name='pago_periodico',
            field=models.DecimalField(decimal_places=2, default=500, help_text='Cuanto pagara en cada semana, quincena o mes', max_digits=7),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pagosalumno',
            name='cancelado',
            field=models.BooleanField(default=False, help_text='Si un pago es cancelado activa esta casilla'),
        ),
        migrations.AlterField(
            model_name='pagosalumno',
            name='forma_de_pago',
            field=models.CharField(choices=[('Efectivo', 'Efectivo'), ('Deposito', 'Deposito'), ('Transferencia', 'Transferencia'), ('Cheque', 'Cheque'), ('Otro', 'Otro')], default='Efectivo', max_length=10),
        ),
        migrations.AlterField(
            model_name='tarjeton',
            name='monto',
            field=models.DecimalField(decimal_places=2, help_text='Aqui ingresa el monto total del servicio', max_digits=7),
        ),
    ]
