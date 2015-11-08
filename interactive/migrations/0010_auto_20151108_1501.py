# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0009_adventdoor_content_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adventdoor',
            name='short_description',
            field=models.CharField(max_length=200, verbose_name='Kort beskrivelse', blank=True, null=True),
        ),
    ]
