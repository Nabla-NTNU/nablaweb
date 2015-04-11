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
                ('open_for', models.ManyToManyField(help_text='Hvilke grupper som får lov til å melde seg på arrangementet. Hvis ingen grupper er valgt er det åpent for alle.', to='auth.Group', null=True, verbose_name='åpen for', blank=True)),
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
                ('number', models.PositiveIntegerField(help_text='Kønummer for ventelisten. Tallene har ingen funksjon dersom man ikke har venteliste på arrangementet.', null=True, verbose_name='kønummer', blank=True)),
                ('attending', models.BooleanField(default=True, help_text='Hvis denne er satt til sann har man en plass på arrangementet ellers er det en ventelisteplass.', verbose_name='har plass')),
                ('event', models.ForeignKey(to='events.Event', null=True)),
                ('user', models.ForeignKey(verbose_name='bruker', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'påmelding',
                'verbose_name_plural': 'påmeldte',
            },
            bases=(models.Model,),
        ),
    ]
