# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nabladet', '0002_nablad_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='nablad',
            name='is_public',
            field=models.BooleanField(verbose_name='tilgjengelighet', help_text='Offentlig tilgjengelighet', default=False),
        ),
    ]
