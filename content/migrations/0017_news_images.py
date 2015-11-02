# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0016_contentimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='images',
            field=models.ManyToManyField(verbose_name='Tilkoblede bilder', to='content.ContentImage'),
        ),
    ]
