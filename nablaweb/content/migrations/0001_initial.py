# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(verbose_name='Publiseringsdato', auto_now_add=True, null=True)),
                ('last_changed_date', models.DateTimeField(verbose_name='Redigeringsdato', auto_now=True, null=True)),
                ('title', models.CharField(verbose_name='Albumtittel', max_length=100, null=True)),
                ('visibillity', models.CharField(choices=[('p', 'public'), ('u', 'users'), ('h', 'hidden')], verbose_name='Synlighet', max_length=1, default='h')),
                ('created_by', models.ForeignKey(verbose_name='Opprettet av', null=True, blank=True, to=settings.AUTH_USER_MODEL, editable=False, related_name='album_created')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AlbumImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('file', filebrowser.fields.FileBrowseField(verbose_name='Bildefil', max_length=100)),
                ('description', models.TextField(blank=True, verbose_name='Bildetekst', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='album',
            name='images',
            field=models.ManyToManyField(verbose_name='Bilder', to='content.AlbumImage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='last_changed_by',
            field=models.ForeignKey(verbose_name='Endret av', null=True, blank=True, to=settings.AUTH_USER_MODEL, editable=False, related_name='album_edited'),
            preserve_default=True,
        ),
    ]
