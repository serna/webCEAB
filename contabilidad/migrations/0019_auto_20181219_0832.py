# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-19 14:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0018_auto_20181218_0859'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorteCaja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folio', models.IntegerField()),
                ('fecha_inicio', models.DateField(default=django.utils.timezone.now)),
                ('fecha_fin', models.DateField(default=django.utils.timezone.now)),
                ('monto_recibido', models.DecimalField(decimal_places=2, help_text='Cantidad de dinero que se recibio en el corte de caja', max_digits=7)),
                ('observaciones', models.TextField(blank=True, help_text='Descripcion breve del corte de caja', max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Cortes de caja',
            },
        ),
        migrations.AlterField(
            model_name='tarjeton',
            name='descripcion',
            field=models.TextField(blank=True, help_text='Descripcion breve relativa al tarjeton', max_length=200),
        ),
        migrations.AlterField(
            model_name='tarjeton',
            name='deuda_actual',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Esta es la cantidad de dinero que debe actualmente el alumno', max_digits=7),
        ),
    ]
