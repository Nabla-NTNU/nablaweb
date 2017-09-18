# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0012_auto_20151103_0013'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='allow_comments',
            field=models.BooleanField(default=True, verbose_name='Tillat kommentarer', help_text='Hvorvidt kommentering er tillatt'),
        ),
    ]
