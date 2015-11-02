# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0018_auto_20151102_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='images',
        ),
        migrations.RemoveField(
            model_name='contentimage',
            name='description',
        ),
        migrations.RemoveField(
            model_name='news',
            name='images',
        ),
    ]
