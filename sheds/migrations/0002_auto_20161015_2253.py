# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-15 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheds', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='day',
            name='date',
        ),
        migrations.AddField(
            model_name='day',
            name='week_even',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='day',
            name='week_odd',
            field=models.BooleanField(default=True),
        ),
    ]
