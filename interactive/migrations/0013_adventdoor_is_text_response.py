# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0012_auto_20151110_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='adventdoor',
            name='is_text_response',
            field=models.BooleanField(default=False, verbose_name='Har tekstsvar'),
        ),
    ]
