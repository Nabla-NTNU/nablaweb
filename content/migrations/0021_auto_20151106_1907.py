# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0020_auto_20151102_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='allow_comments',
        ),
        migrations.RemoveField(
            model_name='news',
            name='content_type',
        ),
    ]
