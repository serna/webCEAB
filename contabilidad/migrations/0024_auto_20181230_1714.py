# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-30 23:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0023_auto_20181229_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cortecaja',
            name='folio',
            field=models.CharField(default='0000', max_length=10),
        ),
    ]
