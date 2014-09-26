# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
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
                ('open_for', models.ManyToManyField(help_text=b'Hvilke grupper som f\xc3\xa5r lov til \xc3\xa5 melde seg p\xc3\xa5 arrangementet. Hvis ingen grupper er valgt er det \xc3\xa5pent for alle.', to='auth.Group', null=True, verbose_name=b'\xc3\x85pen for', blank=True)),
            ],
            options={
                'verbose_name': 'arrangement',
                'verbose_name_plural': 'arrangement',
                'permissions': (('administer', 'Can administer events'),),
            },
            bases=('news.news',),
        ),
        migrations.CreateModel(
            name='EventPenalty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(to='events.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('number', models.PositiveIntegerField(help_text=b'K\xc3\xb8nummer for ventelisten. Tallene har ingen funksjon dersom man ikke har venteliste p\xc3\xa5 arrangementet.', null=True, verbose_name=b'k\xc3\xb8nummer', blank=True)),
                ('attending', models.BooleanField(default=True, help_text=b'Hvis denne er satt til sann har man en plass p\xc3\xa5 arrangementet ellers er det en ventelisteplass.', verbose_name=b'har plass')),
                ('event', models.ForeignKey(to='events.Event', null=True)),
                ('user', models.ForeignKey(verbose_name=b'bruker', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'p\xe5melding',
                'verbose_name_plural': 'p\xe5meldte',
            },
            bases=(models.Model,),
        ),
    ]
