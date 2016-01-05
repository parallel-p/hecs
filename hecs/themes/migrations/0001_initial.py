# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 07:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('href', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='ReferenceGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('icon', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='ReferenceTarget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('color', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=30)),
                ('x', models.IntegerField(null=True)),
                ('y', models.IntegerField(null=True)),
                ('color', models.CharField(blank=True, default='', max_length=6)),
            ],
        ),
        migrations.AddField(
            model_name='reference',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='themes.ReferenceGroup'),
        ),
        migrations.AddField(
            model_name='reference',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='themes.Theme'),
        ),
        migrations.AddField(
            model_name='reference',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='themes.ReferenceTarget'),
        ),
    ]