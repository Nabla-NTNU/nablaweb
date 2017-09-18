# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0002_auto_20150214_2044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='podcast',
            options={'verbose_name_plural': 'Podcast', 'verbose_name': 'Podcast'},
        ),
        migrations.AddField(
            model_name='podcast',
            name='view_counter',
            field=models.IntegerField(editable=False, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='podcast',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name='publisert', auto_now_add=True),
            preserve_default=True,
        ),
    ]
