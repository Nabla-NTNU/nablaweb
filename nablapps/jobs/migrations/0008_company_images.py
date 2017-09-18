# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0018_auto_20151102_2115'),
        ('jobs', '0007_auto_20151102_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='images',
            field=models.ManyToManyField(to='content.ContentImage', verbose_name='Tilkoblede bilder'),
        ),
    ]
