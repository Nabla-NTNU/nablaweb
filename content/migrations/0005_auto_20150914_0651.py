# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_blog_blogpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.SlugField(null=True, help_text='Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres', unique=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='created',
            field=models.DateField(editable=False, verbose_name='Opprettet'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(help_text='Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres', unique=True),
        ),
    ]
