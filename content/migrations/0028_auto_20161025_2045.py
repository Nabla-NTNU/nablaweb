# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0027_blogpost_list_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='edit_listeners',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='edit_listeners',
        ),
        migrations.RemoveField(
            model_name='news',
            name='edit_listeners',
        ),
    ]
