# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 13:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_auto_20160419_2121'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationinfomodel',
            name='place',
            field=models.OneToOneField(default='25#324', on_delete=django.db.models.deletion.CASCADE, to='register.PlaceModel'),
        ),
    ]
