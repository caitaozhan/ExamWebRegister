# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-22 02:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20160419_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='head_image',
            field=models.ImageField(default='accounts/headImageFolder/fuckFu.jpg', upload_to='accounts/headImageFolder/'),
        ),
    ]
