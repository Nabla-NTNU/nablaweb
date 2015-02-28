# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='podcast',
            options={'verbose_name': 'Skr\xe5ttcast', 'verbose_name_plural': 'Skr\xe5ttcast'},
        ),
    ]
