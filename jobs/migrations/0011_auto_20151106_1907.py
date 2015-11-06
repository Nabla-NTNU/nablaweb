# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_auto_20151103_0013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='allow_comments',
        ),
        migrations.RemoveField(
            model_name='company',
            name='content_type',
        ),
    ]
