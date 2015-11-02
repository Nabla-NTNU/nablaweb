# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0017_news_images'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contentimage',
            options={'verbose_name_plural': 'Innholdsbilder', 'verbose_name': 'Innholdsbilde'},
        ),
        migrations.AddField(
            model_name='blogpost',
            name='images',
            field=models.ManyToManyField(to='content.ContentImage', verbose_name='Tilkoblede bilder'),
        ),
    ]
