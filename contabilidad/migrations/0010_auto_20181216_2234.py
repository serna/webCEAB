# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-17 04:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0009_auto_20181216_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarjeton',
            name='descripcion',
            field=models.TextField(default='Creacion: 2018-12-17 04:34', help_text='Descripcion breve relativa al tarjeton', max_length=200),
        ),
    ]
