# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0010_auto_20170911_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='thisUserDownVote',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='thisUserUpVote',
            field=models.BooleanField(default=False),
        ),
    ]
