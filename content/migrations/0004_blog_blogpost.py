# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0003_auto_20150813_2043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', models.DateField(verbose_name='Opprettet', auto_created=True)),
                ('name', models.CharField(max_length=80, verbose_name='Navn')),
            ],
            options={
                'verbose_name': 'Blogg',
                'verbose_name_plural': 'Blogger',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created_date', models.DateTimeField(null=True, verbose_name='Publiseringsdato', auto_now_add=True)),
                ('last_changed_date', models.DateTimeField(null=True, verbose_name='Redigeringsdato', auto_now=True)),
                ('title', models.CharField(max_length=80, verbose_name='Tittel')),
                ('content', models.TextField(verbose_name='Innhold')),
                ('slug', models.SlugField(help_text='Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres')),
                ('allow_comments', models.BooleanField(help_text='Hvorvidt kommentering er tillatt', default=True, verbose_name='Tillat kommentarer')),
                ('blog', models.ForeignKey(verbose_name='Blogg', to='content.Blog')),
                ('created_by', models.ForeignKey(null=True, verbose_name='Opprettet av', blank=True, editable=False, to=settings.AUTH_USER_MODEL, related_name='blogpost_created')),
                ('last_changed_by', models.ForeignKey(null=True, verbose_name='Endret av', blank=True, editable=False, to=settings.AUTH_USER_MODEL, related_name='blogpost_edited')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Poster',
            },
        ),
    ]
