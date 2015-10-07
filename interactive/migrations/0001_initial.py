# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('com', '0003_auto_20151007_1436'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdventCalendar',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('year', models.IntegerField(unique=True, verbose_name='År')),
                ('template', models.CharField(max_length=100, verbose_name='Template', default='interactive/advent_base.html')),
            ],
            options={
                'verbose_name_plural': 'Adventskalendere',
                'verbose_name': 'Adventskalender',
            },
        ),
        migrations.CreateModel(
            name='AdventDoor',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('view_counter', models.IntegerField(editable=False, verbose_name='Visninger', default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Publiseringsdato', null=True)),
                ('last_changed_date', models.DateTimeField(auto_now=True, verbose_name='Redigeringsdato', null=True)),
                ('template', models.CharField(max_length=100, verbose_name='Template', default='interactive/advent_door_base.html')),
                ('number', models.IntegerField(unique=True, verbose_name='Nummer')),
                ('content', models.TextField(blank=True, verbose_name='Innhold')),
                ('calendar', models.ForeignKey(to='interactive.AdventCalendar', verbose_name='Kalender')),
                ('committee', models.ForeignKey(verbose_name='Komité', null=True, blank=True, to='com.Committee')),
                ('created_by', models.ForeignKey(editable=False, verbose_name='Opprettet av', null=True, related_name='adventdoor_created', blank=True, to=settings.AUTH_USER_MODEL)),
                ('edit_listeners', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, help_text='Brukere som overvåker dette objektet', verbose_name='Lyttere')),
                ('last_changed_by', models.ForeignKey(editable=False, verbose_name='Endret av', null=True, related_name='adventdoor_edited', blank=True, to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='advent_participating', blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Deltagende brukere')),
                ('winner', models.ForeignKey(verbose_name='Vinner', null=True, related_name='advent_doors_won', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Adventsluker',
                'verbose_name': 'Adventsluke',
            },
        ),
    ]
