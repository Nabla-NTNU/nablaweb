# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'tittel')),
                ('description', models.TextField(help_text=b'Tekst. Man kan her bruke <a href="http://en.wikipedis.org/wiki/Markdown"target="_blank">markdown</a> for \xc3\xa5 formatere teksten.', verbose_name=b'beskrivelse', blank=True)),
                ('pub_date', models.DateTimeField(help_text=b'Publikasjonsdato', null=True, verbose_name=b'publisert')),
                ('file', models.FileField(help_text=b'Filformat: MP3', upload_to=b'podcast', verbose_name=b'lydfil')),
            ],
            options={
                'verbose_name': 'podcast',
                'verbose_name_plural': 'podcasts',
            },
            bases=(models.Model,),
        ),
    ]
