# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0003_connectionurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='connectionurl',
            name='db',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
