# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-09 09:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_parser', '0005_auto_20160809_0658'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postdata',
            old_name='group',
            new_name='forumAlias',
        ),
        migrations.AddField(
            model_name='postdata',
            name='forumName',
            field=models.CharField(default='default', max_length=255),
            preserve_default=False,
        ),
    ]
