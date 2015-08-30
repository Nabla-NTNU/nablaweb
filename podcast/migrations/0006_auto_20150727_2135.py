# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0005_auto_20150727_2133'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='season',
            options={'verbose_name': 'Sesong', 'verbose_name_plural': 'Sesonger'},
        ),
    ]
