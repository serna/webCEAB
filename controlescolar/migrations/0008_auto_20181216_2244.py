# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-17 04:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controlescolar', '0007_auto_20181216_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materia',
            name='plantel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='siad.Calendario'),
        ),
    ]
