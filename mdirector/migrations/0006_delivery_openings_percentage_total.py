# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-12 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdirector', '0005_auto_20160408_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='openings_percentage_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
            preserve_default=False,
        ),
    ]
