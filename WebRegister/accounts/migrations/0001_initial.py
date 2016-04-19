# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 11:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('register', '0001_initial'),
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationInfoModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_number', models.CharField(max_length=30)),
                ('is_paid', models.BooleanField(default=False)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.ExamInfoModel')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('id_number', models.CharField(max_length=30, unique=True)),
                ('gender', models.CharField(choices=[('男', '男'), ('女', '女')], max_length=6)),
                ('phone', models.CharField(max_length=20)),
                ('exam', models.ManyToManyField(through='accounts.RegistrationInfoModel', to='register.ExamInfoModel')),
            ],
        ),
        migrations.AddField(
            model_name='registrationinfomodel',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Student'),
        ),
    ]
