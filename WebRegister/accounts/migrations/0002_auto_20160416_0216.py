# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-16 02:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StudentInfoModel',
            new_name='Student',
        ),
    ]
