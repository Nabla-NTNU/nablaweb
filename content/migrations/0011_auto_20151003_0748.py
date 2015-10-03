# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0010_auto_20151003_0657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='published',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='published',
        ),
        migrations.RemoveField(
            model_name='news',
            name='published',
        ),
    ]
