# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0007_auto_20150727_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='logo',
            field=models.ImageField(upload_to='podcast/images', blank=True, null=True, help_text='Podcastlogo.', verbose_name='Logo'),
            preserve_default=True,
        ),
    ]
