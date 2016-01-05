# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='color',
        ),
        migrations.AddField(
            model_name='theme',
            name='category',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]