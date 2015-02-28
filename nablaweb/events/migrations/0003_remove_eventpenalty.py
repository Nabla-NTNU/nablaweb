# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20141013_1716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventpenalty',
            name='event',
        ),
        migrations.RemoveField(
            model_name='eventpenalty',
            name='user',
        ),
        migrations.DeleteModel(
            name='EventPenalty',
        )
    ]
