# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BedPres',
            fields=[
                ('news_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='news.News')),
                ('short_name', models.CharField(help_text=b'Brukes p\xc3\xa5 steder hvor det ikke er plass til \xc3\xa5 skrive hele overskriften, for eksempel kalenderen.', max_length=20, null=True, verbose_name=b'kort navn', blank=True)),
                ('organizer', models.CharField(help_text=b'Den som st\xc3\xa5r bak arrangementet', max_length=100, verbose_name=b'organisert av', blank=True)),
                ('location', models.CharField(max_length=100, verbose_name='sted')),
                ('event_start', models.DateTimeField(null=True, verbose_name=b'start')),
                ('event_end', models.DateTimeField(null=True, verbose_name=b'slutt', blank=True)),
                ('registration_required', models.BooleanField(default=False, verbose_name=b'p\xc3\xa5melding')),
                ('registration_deadline', models.DateTimeField(null=True, verbose_name=b'p\xc3\xa5meldingsfrist', blank=True)),
                ('registration_start', models.DateTimeField(null=True, verbose_name=b'p\xc3\xa5melding \xc3\xa5pner', blank=True)),
                ('deregistration_deadline', models.DateTimeField(null=True, verbose_name=b'avmelding stenger', blank=True)),
                ('places', models.PositiveIntegerField(null=True, verbose_name=b'antall plasser', blank=True)),
                ('has_queue', models.NullBooleanField(help_text=b'Om ventelisten er p\xc3\xa5, vil det v\xc3\xa6re mulig \xc3\xa5 melde seg p\xc3\xa5 selv om arrangementet er fullt. De som er i ventelisten vil automatisk bli p\xc3\xa5meldt etter hvert som plasser blir ledige.', verbose_name=b'har venteliste')),
                ('facebook_url', models.CharField(help_text=b'URL-en til det tilsvarende arrangementet p\xc3\xa5 Facebook', max_length=100, verbose_name=b'facebook-url', blank=True)),
                ('bpcid', models.CharField(help_text=b"Dette er id'en som blir brukt internt hos BPC. Ikke endre den hvis du ikke vet du gj\xc3\xb8r.", unique=True, max_length=16, verbose_name=b'BPC-id')),
            ],
            options={
                'verbose_name': 'bedriftspresentasjon',
                'verbose_name_plural': 'bedriftspresentasjoner',
            },
            bases=('news.news',),
        ),
    ]
