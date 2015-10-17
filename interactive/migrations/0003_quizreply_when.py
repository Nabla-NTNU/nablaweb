# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0002_auto_20151016_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizreply',
            name='when',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 17, 21, 30, 20, 38594), auto_created=True),
            preserve_default=False,
        ),
    ]
