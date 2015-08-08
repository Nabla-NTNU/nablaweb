# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date', models.DateTimeField(null=True, verbose_name='Påmeldingsdato', auto_now_add=True)),
                ('number', models.PositiveIntegerField(null=True, verbose_name='kønummer', blank=True, help_text='Kønummer som tilsvarer plass på ventelisten/påmeldingsrekkefølge.')),
                ('attending', models.BooleanField(verbose_name='har plass', default=True, help_text='Hvis denne er satt til sann har man en plass på arrangementet ellers er det en ventelisteplass.')),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, verbose_name='bruker')),
            ],
            options={
                'verbose_name': 'påmelding',
                'verbose_name_plural': 'påmeldte',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created_date', models.DateTimeField(null=True, verbose_name='Publiseringsdato', auto_now_add=True)),
                ('last_changed_date', models.DateTimeField(null=True, verbose_name='Redigeringsdato', auto_now=True)),
                ('picture', models.ImageField(null=True, verbose_name='Bilde', blank=True, upload_to='news_pictures', help_text='Bilder som er større enn 770x300 px ser best ut. Du kan beskjære bildet etter opplasting.')),
                ('cropping', image_cropping.fields.ImageRatioField('picture', '770x300', hide_image_field=False, help_text=None, verbose_name='Beskjæring', free_crop=False, size_warning=False, adapt_rotation=False, allow_fullsize=False)),
                ('slug', models.SlugField(null=True, blank=True, help_text='Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres')),
                ('allow_comments', models.BooleanField(verbose_name='Tillat kommentarer', default=True, help_text='Hvorvidt kommentering er tillatt')),
                ('headline', models.CharField(verbose_name='tittel', max_length=100)),
                ('lead_paragraph', models.TextField(verbose_name='ingress', blank=True, help_text='Vises på forsiden og i artikkelen')),
                ('body', models.TextField(verbose_name='brødtekst', blank=True, help_text='Vises kun i artikkelen. Man kan her bruke <a href="http://en.wikipedia.org/wiki/Markdown" target="_blank">markdown</a> for å formatere teksten.')),
                ('priority', models.IntegerField(verbose_name='Prioritering', choices=[(0, '0 - Dukker ikke opp'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10 - Er på forsida hele tiden')], default=5, help_text='Prioritering av saken på forsiden. Dette fungerer for øyeblikket ikke. Bortsett fra at prioritering=0 fjerner saken fra forsiden.')),
            ],
            options={
                'verbose_name': 'nyhet',
                'verbose_name_plural': 'nyheter',
            },
        ),
        migrations.AlterModelOptions(
            name='album',
            options={'verbose_name': 'Album', 'verbose_name_plural': 'Album'},
        ),
        migrations.AlterModelOptions(
            name='albumimage',
            options={'verbose_name': 'Albumbilde', 'verbose_name_plural': 'Albumbilder'},
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('news_ptr', models.OneToOneField(auto_created=True, parent_link=True, primary_key=True, serialize=False, to='content.News')),
                ('short_name', models.CharField(null=True, verbose_name='kort navn', blank=True, max_length=20, help_text='Brukes på steder hvor det ikke er plass til å skrive hele overskriften, for eksempel kalenderen.')),
                ('organizer', models.CharField(verbose_name='organisert av', blank=True, max_length=100, help_text='Den som står bak arrangementet')),
                ('location', models.CharField(verbose_name='sted', max_length=100)),
                ('event_start', models.DateTimeField(null=True, verbose_name='start')),
                ('event_end', models.DateTimeField(null=True, verbose_name='slutt', blank=True)),
                ('facebook_url', models.CharField(verbose_name='facebook-url', blank=True, max_length=100, help_text='URL-en til det tilsvarende arrangementet på Facebook')),
                ('registration_required', models.BooleanField(verbose_name='påmelding', default=False)),
                ('registration_deadline', models.DateTimeField(null=True, verbose_name='påmeldingsfrist', blank=True)),
                ('registration_start', models.DateTimeField(null=True, verbose_name='påmelding åpner', blank=True)),
                ('deregistration_deadline', models.DateTimeField(null=True, verbose_name='avmeldingsfrist', blank=True)),
                ('places', models.PositiveIntegerField(null=True, verbose_name='antall plasser', blank=True)),
                ('has_queue', models.NullBooleanField(verbose_name='har venteliste', help_text='Om ventelisten er på, vil det være mulig å melde seg på selv om arrangementet er fullt. De som er i ventelisten vil automatisk bli påmeldt etter hvert som plasser blir ledige.')),
                ('open_for', models.ManyToManyField(null=True, verbose_name='Åpen for', to='auth.Group', blank=True, help_text='Hvilke grupper som får lov til å melde seg på arrangementet. Hvis ingen grupper er valgt er det åpent for alle.')),
            ],
            options={
                'verbose_name': 'arrangement',
                'verbose_name_plural': 'arrangement',
                'permissions': (('administer', 'Can administer events'),),
            },
            bases=('content.news', models.Model),
        ),
        migrations.AddField(
            model_name='news',
            name='content_type',
            field=models.ForeignKey(null=True, to='contenttypes.ContentType', editable=False),
        ),
        migrations.AddField(
            model_name='news',
            name='created_by',
            field=models.ForeignKey(null=True, blank=True, verbose_name='Opprettet av', editable=False, to=settings.AUTH_USER_MODEL, related_name='news_created'),
        ),
        migrations.AddField(
            model_name='news',
            name='last_changed_by',
            field=models.ForeignKey(null=True, blank=True, verbose_name='Endret av', editable=False, to=settings.AUTH_USER_MODEL, related_name='news_edited'),
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='event',
            field=models.ForeignKey(null=True, to='content.Event'),
        ),
        migrations.AlterUniqueTogether(
            name='eventregistration',
            unique_together=set([('number', 'attending'), ('event', 'user')]),
        ),
    ]
