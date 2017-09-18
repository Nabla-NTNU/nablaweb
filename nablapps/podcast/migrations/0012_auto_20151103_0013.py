# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0011_auto_20151102_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcast',
            name='published',
            field=models.NullBooleanField(help_text='Dato har høyere prioritet enn dette feltet.', verbose_name='Publisert', default=True),
        ),
    ]
