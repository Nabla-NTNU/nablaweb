# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0006_adventdoor_participating_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='adventdoor',
            name='short_description',
            field=models.CharField(null=True, max_length=200, verbose_name='Kort beskrivelse'),
        ),
    ]
