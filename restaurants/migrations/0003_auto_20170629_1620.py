# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_auto_20170629_1328'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='restaurants',
            new_name='restaurant',
        ),
    ]
