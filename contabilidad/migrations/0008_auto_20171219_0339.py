# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-19 03:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0007_auto_20171219_0308'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Egreso',
            new_name='EgresoGenerales',
        ),
        migrations.RenameModel(
            old_name='Egreso_nomina',
            new_name='EgresoNomina',
        ),
    ]
