# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
        ('jobs', '0001_squashed_0012_auto_20151106_1921'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='BedPres',
            fields=[
                ('news_ptr', models.OneToOneField(to='news.News', primary_key=True, parent_link=True, serialize=False, auto_created=True)),
                ('short_name', models.CharField(help_text='Brukes på steder hvor det ikke er plass til å skrive hele overskriften, for eksempel kalenderen.', blank=True, max_length=20, null=True, verbose_name='kort navn')),
                ('organizer', models.CharField(help_text='Den som står bak arrangementet', blank=True, max_length=100, verbose_name='organisert av')),
                ('location', models.CharField(max_length=100, verbose_name='sted')),
                ('event_start', models.DateTimeField(null=True, verbose_name='start')),
                ('event_end', models.DateTimeField(blank=True, null=True, verbose_name='slutt')),
                ('facebook_url', models.CharField(help_text='URL-en til det tilsvarende arrangementet på Facebook', blank=True, max_length=100, verbose_name='facebook-url')),
                ('registration_required', models.BooleanField(default=False, verbose_name='påmelding')),
                ('registration_deadline', models.DateTimeField(blank=True, null=True, verbose_name='påmeldingsfrist')),
                ('registration_start', models.DateTimeField(blank=True, null=True, verbose_name='påmelding åpner')),
                ('deregistration_deadline', models.DateTimeField(blank=True, null=True, verbose_name='avmeldingsfrist')),
                ('places', models.PositiveIntegerField(blank=True, null=True, verbose_name='antall plasser')),
                ('has_queue', models.NullBooleanField(help_text='Om ventelisten er på, vil det være mulig å melde seg på selv om arrangementet er fullt. De som er i ventelisten vil automatisk bli påmeldt etter hvert som plasser blir ledige.', verbose_name='har venteliste')),
                ('bpcid', models.CharField(help_text="Dette er id'en som blir brukt internt hos BPC. Ikke endre den hvis du ikke vet du gjør.", max_length=16, unique=True, verbose_name='BPC-id')),
                ('company', models.ForeignKey(help_text='Hvilken bedrift som står bak bedriftspresentasjonen', to='jobs.Company', verbose_name='Bedrift')),
                ('open_for', models.ManyToManyField(help_text='Hvilke grupper som får lov til å melde seg på arrangementet. Hvis ingen grupper er valgt er det åpent for alle.', blank=True, to='auth.Group', verbose_name='Åpen for')),
            ],
            options={
                'verbose_name': 'bedriftspresentasjon',
                'verbose_name_plural': 'bedriftspresentasjoner',
            },
            bases=('news.news', models.Model),
        ),
    ]
