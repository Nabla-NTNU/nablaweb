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
                ('title', models.CharField(max_length=200, verbose_name='tittel')),
                ('description', models.TextField(help_text='Tekst. Man kan her bruke <a href="http://en.wikipedis.org/wiki/Markdown"target="_blank">markdown</a> for å formatere teksten.', verbose_name='beskrivelse', blank=True)),
                ('pub_date', models.DateTimeField(help_text='Publikasjonsdato', null=True, verbose_name='publisert')),
                ('file', models.FileField(help_text='Filformat: MP3', upload_to='podcast', verbose_name='lydfil')),
            ],
            options={
                'verbose_name': 'podcast',
                'verbose_name_plural': 'podcasts',
            },
            bases=(models.Model,),
        ),
    ]
