# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_auto_20170630_1018'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=255)),
                ('visitor', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('date_time', models.DateTimeField()),
                ('restaurant', models.ForeignKey(to='restaurants.Restaurant')),
            ],
        ),
    ]
