# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-19 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siad', '0006_calendario'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactoempresarial',
            name='extension',
            field=models.CharField(default='0000', max_length=10),
        ),
        migrations.AddField(
            model_name='contactoempresarial',
            name='telefono',
            field=models.CharField(default='000 000 0000', max_length=20),
        ),
    ]
