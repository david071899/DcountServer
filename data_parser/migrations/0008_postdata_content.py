# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-09 09:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_parser', '0007_auto_20160809_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='postdata',
            name='content',
            field=models.TextField(default='default'),
            preserve_default=False,
        ),
    ]
