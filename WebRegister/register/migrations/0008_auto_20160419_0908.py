# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 01:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0007_auto_20160419_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinfomodel',
            name='exam_time_end',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 19, 1, 8, 14, 902034, tzinfo=utc)),
        ),
    ]
