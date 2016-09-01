# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0002_auto_20160828_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='land',
            field=models.CharField(verbose_name='land', default='', help_text='Landet universitetet ligger i', max_length=30),
        ),
    ]
