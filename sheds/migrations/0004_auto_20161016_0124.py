# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-15 22:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheds', '0003_auto_20161015_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='name',
            field=models.CharField(max_length=32, verbose_name='weekday'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='name',
            field=models.CharField(max_length=200, verbose_name='lesson name'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='week_even',
            field=models.BooleanField(default=False, verbose_name='whether even week lesson'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='week_odd',
            field=models.BooleanField(default=False, verbose_name='whether odd week lesson'),
        ),
    ]
