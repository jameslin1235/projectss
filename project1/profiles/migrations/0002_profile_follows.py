# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-30 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(null=True, related_name='_profile_follows_+', to='profiles.Profile'),
        ),
    ]
