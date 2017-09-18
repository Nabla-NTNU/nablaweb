# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_squashed_0012_auto_20151106_1921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='edit_listeners',
        ),
    ]
