# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-14 15:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_auto_20160414_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentinfomodel',
            name='user',
        ),
        migrations.DeleteModel(
            name='StudentInfoModel',
        ),
    ]
