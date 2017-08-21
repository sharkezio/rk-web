# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('price', models.DecimalField(max_digits=3, decimal_places=0)),
                ('comment', models.CharField(max_length=50, blank=True)),
                ('is_spicy', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=50, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='food',
            name='Restaurants',
            field=models.ForeignKey(to='restaurants.Restaurant'),
        ),
    ]
