# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0008_season_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcast',
            name='description',
            field=models.TextField(help_text='Teksten vil bli kuttet etter 250 tegn på sesongsiden.', verbose_name='beskrivelse', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='podcast',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name='publisert'),
            preserve_default=True,
        ),
    ]
