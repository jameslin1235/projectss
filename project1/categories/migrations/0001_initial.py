# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
    ]
