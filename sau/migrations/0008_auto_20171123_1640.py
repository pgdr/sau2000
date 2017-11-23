# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sau', '0007_sheep_end'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sheep',
            name='end',
        ),
        migrations.AddField(
            model_name='sheep',
            name='dead',
            field=models.DateTimeField(blank=True, null=True, verbose_name='death'),
        ),
        migrations.AddField(
            model_name='sheep',
            name='removed',
            field=models.DateTimeField(blank=True, null=True, verbose_name='removed'),
        ),
    ]
