# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-18 18:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitortrack',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 3, 18, 18, 17, 17, 466555)),
            preserve_default=False,
        ),
    ]
