# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0025_auto_20160103_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='albumimage',
            name='num',
            field=models.PositiveIntegerField(null=True, verbose_name='Nummer'),
        ),
    ]
