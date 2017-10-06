# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_auto_20170629_1620'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='food',
            options={'ordering': ['price']},
        ),
    ]
