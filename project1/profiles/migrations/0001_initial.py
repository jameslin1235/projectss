# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-18 22:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import project1.project1.profiles.models


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
                ('first_login', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('gender', models.CharField(blank=True, choices=[('', 'Select a Gender'), ('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('industry', models.CharField(blank=True, max_length=100)),
                ('position', models.CharField(blank=True, max_length=100)),
                ('company', models.CharField(blank=True, max_length=100)),
                ('school', models.CharField(blank=True, max_length=100)),
                ('concentration', models.CharField(blank=True, max_length=100)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('credential', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('avatar_width_field', models.IntegerField()),
                ('avatar_height_field', models.IntegerField()),
                ('avatar', models.ImageField(blank=True, default='default/avatar.jpg', height_field='avatar_height_field', upload_to=project1.project1.profiles.models.get_upload_location, width_field='avatar_width_field')),
                ('background_width_field', models.IntegerField()),
                ('background_height_field', models.IntegerField()),
                ('background', models.ImageField(blank=True, default='default/background.jpg', height_field='background_height_field', upload_to=project1.project1.profiles.models.get_upload_location, width_field='background_width_field')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='ProfileFollow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_followed', models.DateTimeField()),
                ('dest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dest', to='profiles.Profile')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='profiles.Profile')),
            ],
            options={
                'ordering': ['-date_followed'],
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='profiles.ProfileFollow', to='profiles.Profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
