# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 17:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=140)),
                ('author_email', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(null=True)),
                ('state', models.CharField(choices=[('pending', 'pending'), ('published', 'published'), ('rejected', 'rejected')], max_length=15)),
            ],
            options={
                'permissions': (('can_approve_or_reject_tweet', 'can approve or reject twwets'),),
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='tweet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poster.Tweet'),
        ),
    ]