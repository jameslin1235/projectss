# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-30 20:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0018_auto_20170530_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
    ]
