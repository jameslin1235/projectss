# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-10 02:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import project1.project1.topics.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('image', models.ImageField(blank=True, null=True, upload_to=project1.project1.topics.models.get_upload_location)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TopicUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_followed', models.DateTimeField()),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topics.Topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='topic',
            name='followers',
            field=models.ManyToManyField(null=True, related_name='followed_topics', through='topics.TopicUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
