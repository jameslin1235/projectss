# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 18:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=100)),
                ('company', models.CharField(blank=True, max_length=100)),
                ('school', models.CharField(blank=True, max_length=100)),
                ('concentration', models.CharField(blank=True, max_length=100)),
                ('degree_type', models.CharField(blank=True, max_length=100)),
                ('avatar', models.FileField(blank=True, default='profile_avatar/1.jpg', upload_to='profile_avatar/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]
