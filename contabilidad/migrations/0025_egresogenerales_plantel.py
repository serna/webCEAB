# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-04-03 17:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('siad', '0007_auto_20181219_0832'),
        ('contabilidad', '0024_auto_20181230_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='egresogenerales',
            name='plantel',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='siad.Plantel'),
            preserve_default=False,
        ),
    ]