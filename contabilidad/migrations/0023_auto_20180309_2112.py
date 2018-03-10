# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-10 03:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0022_auto_20180309_2111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tarjeton',
            old_name='movimiento_verificado_por_direccion',
            new_name='tarjeton_verificado_por_direccion',
        ),
        migrations.AlterField(
            model_name='tarjeton',
            name='descripcion',
            field=models.CharField(default='Creacion: <function now at 0x7f739eb667b8>', help_text='Descripcion breve relativa al tarjeton', max_length=100),
        ),
    ]
