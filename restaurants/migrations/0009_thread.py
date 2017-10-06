# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0008_auto_20170831_2039'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userDownVotes', models.ManyToManyField(related_name='threadDownVotes', to=settings.AUTH_USER_MODEL, blank=True)),
                ('userUpVotes', models.ManyToManyField(related_name='threadUpVotes', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
    ]
