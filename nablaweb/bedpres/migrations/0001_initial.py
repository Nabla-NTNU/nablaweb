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
                ('short_name', models.CharField(help_text='Brukes på steder hvor det ikke er plass til å skrive hele overskriften, for eksempel kalenderen.', max_length=20, null=True, verbose_name='kort navn', blank=True)),
                ('organizer', models.CharField(help_text='Den som står bak arrangementet', max_length=100, verbose_name='organisert av', blank=True)),
                ('location', models.CharField(max_length=100, verbose_name='sted')),
                ('event_start', models.DateTimeField(null=True, verbose_name='start')),
                ('event_end', models.DateTimeField(null=True, verbose_name='slutt', blank=True)),
                ('registration_required', models.BooleanField(default=False, verbose_name='påmelding')),
                ('registration_deadline', models.DateTimeField(null=True, verbose_name='påmeldingsfrist', blank=True)),
                ('registration_start', models.DateTimeField(null=True, verbose_name='påmelding åpner', blank=True)),
                ('deregistration_deadline', models.DateTimeField(null=True, verbose_name='avmelding stenger', blank=True)),
                ('places', models.PositiveIntegerField(null=True, verbose_name='antall plasser', blank=True)),
                ('has_queue', models.NullBooleanField(help_text='Om ventelisten er på, vil det være mulig å melde seg på selv om arrangementet er fullt. De som er i ventelisten vil automatisk bli påmeldt etter hvert som plasser blir ledige.', verbose_name='har venteliste')),
                ('facebook_url', models.CharField(help_text='URL-en til det tilsvarende arrangementet på Facebook', max_length=100, verbose_name='facebook-url', blank=True)),
                ('bpcid', models.CharField(help_text="Dette er id'en som blir brukt internt hos BPC. Ikke endre den hvis du ikke vet du gjør.", unique=True, max_length=16, verbose_name='BPC-id')),
            ],
            options={
                'verbose_name': 'bedriftspresentasjon',
                'verbose_name_plural': 'bedriftspresentasjoner',
            },
            bases=('news.news',),
        ),
    ]
