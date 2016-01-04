# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0023_splashconfig'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='images',
        ),
        migrations.AddField(
            model_name='albumimage',
            name='album',
            field=models.ForeignKey(to='content.Album', related_name='images', null=True, verbose_name='Album'),
        ),
        migrations.AlterField(
            model_name='splashconfig',
            name='redirect_url',
            field=models.URLField(default='https://example.com', help_text="The URL the users should be redirected to when they don't have the right cookie"),
        ),
    ]
