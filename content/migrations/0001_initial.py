# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields
import image_cropping.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created_date', models.DateTimeField(null=True, auto_now_add=True, verbose_name='Publiseringsdato')),
                ('last_changed_date', models.DateTimeField(null=True, auto_now=True, verbose_name='Redigeringsdato')),
                ('title', models.CharField(null=True, max_length=100, verbose_name='Albumtittel')),
                ('visibillity', models.CharField(default='h', choices=[('p', 'public'), ('u', 'users'), ('h', 'hidden')], max_length=1, verbose_name='Synlighet')),
                ('created_by', models.ForeignKey(null=True, editable=False, blank=True, related_name='album_created', to=settings.AUTH_USER_MODEL, verbose_name='Opprettet av')),
            ],
            options={
                'verbose_name_plural': 'Album',
                'verbose_name': 'Album',
            },
        ),
        migrations.CreateModel(
            name='AlbumImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('file', filebrowser.fields.FileBrowseField(max_length=100, verbose_name='Bildefil')),
                ('description', models.TextField(null=True, blank=True, verbose_name='Bildetekst')),
            ],
            options={
                'verbose_name_plural': 'Albumbilder',
                'verbose_name': 'Albumbilde',
            },
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('date', models.DateTimeField(null=True, auto_now_add=True, verbose_name='Påmeldingsdato')),
                ('number', models.PositiveIntegerField(null=True, help_text='Kønummer som tilsvarer plass på ventelisten/påmeldingsrekkefølge.', blank=True, verbose_name='kønummer')),
                ('attending', models.BooleanField(default=True, help_text='Hvis denne er satt til sann har man en plass på arrangementet ellers er det en ventelisteplass.', verbose_name='har plass')),
                ('user', models.ForeignKey(null=True, verbose_name='bruker', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'påmeldte',
                'verbose_name': 'påmelding',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created_date', models.DateTimeField(null=True, auto_now_add=True, verbose_name='Publiseringsdato')),
                ('last_changed_date', models.DateTimeField(null=True, auto_now=True, verbose_name='Redigeringsdato')),
                ('picture', models.ImageField(null=True, verbose_name='Bilde', help_text='Bilder som er større enn 770x300 px ser best ut. Du kan beskjære bildet etter opplasting.', upload_to='news_pictures', blank=True)),
                ('cropping', image_cropping.fields.ImageRatioField('picture', '770x300', size_warning=False, hide_image_field=False, allow_fullsize=False, verbose_name='Beskjæring', help_text=None, free_crop=False, adapt_rotation=False)),
                ('slug', models.SlugField(null=True, blank=True, help_text='Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres')),
                ('allow_comments', models.BooleanField(default=True, help_text='Hvorvidt kommentering er tillatt', verbose_name='Tillat kommentarer')),
                ('headline', models.CharField(max_length=100, verbose_name='tittel')),
                ('lead_paragraph', models.TextField(help_text='Vises på forsiden og i artikkelen', blank=True, verbose_name='ingress')),
                ('body', models.TextField(help_text='Vises kun i artikkelen. Man kan her bruke <a href="http://en.wikipedia.org/wiki/Markdown" target="_blank">markdown</a> for å formatere teksten.', blank=True, verbose_name='brødtekst')),
                ('priority', models.IntegerField(default=5, help_text='Prioritering av saken på forsiden. Dette fungerer for øyeblikket ikke. Bortsett fra at prioritering=0 fjerner saken fra forsiden.', choices=[(0, '0 - Dukker ikke opp'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10 - Er på forsida hele tiden')], verbose_name='Prioritering')),
            ],
            options={
                'verbose_name_plural': 'nyheter',
                'verbose_name': 'nyhet',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('news_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, auto_created=True, to='content.News')),
                ('short_name', models.CharField(null=True, help_text='Brukes på steder hvor det ikke er plass til å skrive hele overskriften, for eksempel kalenderen.', blank=True, max_length=20, verbose_name='kort navn')),
                ('organizer', models.CharField(help_text='Den som står bak arrangementet', blank=True, max_length=100, verbose_name='organisert av')),
                ('location', models.CharField(max_length=100, verbose_name='sted')),
                ('event_start', models.DateTimeField(null=True, verbose_name='start')),
                ('event_end', models.DateTimeField(null=True, blank=True, verbose_name='slutt')),
                ('facebook_url', models.CharField(help_text='URL-en til det tilsvarende arrangementet på Facebook', blank=True, max_length=100, verbose_name='facebook-url')),
                ('registration_required', models.BooleanField(default=False, verbose_name='påmelding')),
                ('registration_deadline', models.DateTimeField(null=True, blank=True, verbose_name='påmeldingsfrist')),
                ('registration_start', models.DateTimeField(null=True, blank=True, verbose_name='påmelding åpner')),
                ('deregistration_deadline', models.DateTimeField(null=True, blank=True, verbose_name='avmeldingsfrist')),
                ('places', models.PositiveIntegerField(null=True, blank=True, verbose_name='antall plasser')),
                ('has_queue', models.NullBooleanField(help_text='Om ventelisten er på, vil det være mulig å melde seg på selv om arrangementet er fullt. De som er i ventelisten vil automatisk bli påmeldt etter hvert som plasser blir ledige.', verbose_name='har venteliste')),
                ('open_for', models.ManyToManyField(help_text='Hvilke grupper som får lov til å melde seg på arrangementet. Hvis ingen grupper er valgt er det åpent for alle.', blank=True, to='auth.Group', verbose_name='Åpen for')),
            ],
            options={
                'verbose_name_plural': 'arrangement',
                'verbose_name': 'arrangement',
                'permissions': (('administer', 'Can administer events'),),
            },
            bases=('content.news', models.Model),
        ),
        migrations.AddField(
            model_name='news',
            name='content_type',
            field=models.ForeignKey(null=True, editable=False, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='news',
            name='created_by',
            field=models.ForeignKey(null=True, editable=False, blank=True, related_name='news_created', to=settings.AUTH_USER_MODEL, verbose_name='Opprettet av'),
        ),
        migrations.AddField(
            model_name='news',
            name='last_changed_by',
            field=models.ForeignKey(null=True, editable=False, blank=True, related_name='news_edited', to=settings.AUTH_USER_MODEL, verbose_name='Endret av'),
        ),
        migrations.AddField(
            model_name='album',
            name='images',
            field=models.ManyToManyField(to='content.AlbumImage', verbose_name='Bilder'),
        ),
        migrations.AddField(
            model_name='album',
            name='last_changed_by',
            field=models.ForeignKey(null=True, editable=False, blank=True, related_name='album_edited', to=settings.AUTH_USER_MODEL, verbose_name='Endret av'),
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='event',
            field=models.ForeignKey(null=True, to='content.Event'),
        ),
        migrations.AlterUniqueTogether(
            name='eventregistration',
            unique_together=set([('event', 'user'), ('number', 'attending')]),
        ),
    ]
