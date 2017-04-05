# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0001_squashed_0022_adventdoor_user_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adventdoor',
            name='edit_listeners',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='edit_listeners',
        ),
        migrations.RemoveField(
            model_name='test',
            name='edit_listeners',
        ),
    ]
