# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0009_thread'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='userDownVotes',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='userUpVotes',
        ),
        migrations.AddField(
            model_name='comment',
            name='userDownVotes',
            field=models.ManyToManyField(related_name='threadDownVotes', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='userUpVotes',
            field=models.ManyToManyField(related_name='threadUpVotes', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.DeleteModel(
            name='Thread',
        ),
    ]
