# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-13 10:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_student_graduated'),
    ]

    operations = [
        migrations.AddField(
            model_name='presence',
            name='teacher',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.Teacher'),
        ),
    ]
