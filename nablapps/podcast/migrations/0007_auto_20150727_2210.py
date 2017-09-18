# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0006_auto_20150727_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='banner',
            field=models.ImageField(blank=True, help_text='Sesongbanner.', null=True, verbose_name='Banner', upload_to='podcast/images'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='season',
            name='number',
            field=models.IntegerField(verbose_name='Sesongnummer', unique=True),
            preserve_default=True,
        ),
    ]
