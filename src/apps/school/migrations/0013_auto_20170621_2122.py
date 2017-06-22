# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 21:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0012_auto_20170619_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presence',
            name='absence_report',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='absence.AbsenceReport'),
        ),
        migrations.AlterField(
            model_name='presence',
            name='teacher',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.Teacher'),
        ),
    ]