# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 03:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170524_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='import',
            name='origin',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, verbose_name='origem'),
            preserve_default=False,
        ),
    ]