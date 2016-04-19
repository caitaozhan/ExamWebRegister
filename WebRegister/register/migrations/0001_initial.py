# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 11:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExamInfoModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=30, verbose_name='科目名称')),
                ('exam_time', models.DateTimeField(verbose_name='考试开始时间')),
                ('exam_time_end', models.DateTimeField(default=datetime.datetime(2016, 4, 19, 11, 36, 29, 295564, tzinfo=utc), verbose_name='考试结束时间')),
                ('register_deadline', models.DateTimeField(default=django.utils.timezone.now, verbose_name='报名截至时间')),
                ('fee', models.IntegerField(verbose_name='考试费用')),
                ('notes', models.CharField(default='', max_length=512, verbose_name='备注')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='examinfomodel',
            unique_together=set([('subject', 'exam_time')]),
        ),
    ]
