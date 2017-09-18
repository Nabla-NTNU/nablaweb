# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Publiseringsdato', null=True)),
                ('last_changed_date', models.DateTimeField(verbose_name='Redigeringsdato', null=True, auto_now=True)),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Albumtittel')),
                ('visibility', models.CharField(choices=[('p', 'public'), ('u', 'users'), ('h', 'hidden')], max_length=1, verbose_name='Synlighet', default='h')),
                ('created_by', models.ForeignKey(related_name='album_created', editable=False, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Opprettet av', null=True)),
                ('last_changed_by', models.ForeignKey(related_name='album_edited', editable=False, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Endret av', null=True)),
                ('view_counter', models.IntegerField(editable=False, verbose_name='Visninger', default=0)),
            ],
            options={
                'verbose_name': 'Album',
                'verbose_name_plural': 'Album',
            },
        ),
        migrations.CreateModel(
            name='AlbumImage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('file', models.ImageField(verbose_name='Bildefil', upload_to='uploads/content')),
                ('description', models.TextField(blank=True, verbose_name='Bildetekst', null=True)),
                ('album', models.ForeignKey(related_name='images', to='content.Album', verbose_name='Album', null=True)),
                ('num', models.PositiveIntegerField(verbose_name='Nummer', null=True)),
            ],
            options={
                'verbose_name': 'Albumbilde',
                'verbose_name_plural': 'Albumbilder',
            },
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Påmeldingsdato', null=True)),
                ('number', models.PositiveIntegerField(blank=True, help_text='Kønummer som tilsvarer plass på ventelisten/påmeldingsrekkefølge.', verbose_name='kønummer', null=True)),
                ('attending', models.BooleanField(help_text='Hvis denne er satt til sann har man en plass på arrangementet ellers er det en ventelisteplass.', verbose_name='har plass', default=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='bruker', null=True)),
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
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Publiseringsdato', null=True)),
                ('last_changed_date', models.DateTimeField(verbose_name='Redigeringsdato', null=True, auto_now=True)),
                ('picture', models.ImageField(upload_to='uploads/news_pictures', blank=True, help_text='Bilder som er større enn 770x300 px ser best ut. Du kan beskjære bildet etter opplasting.', verbose_name='Bilde', null=True)),
                ('cropping', image_cropping.fields.ImageRatioField('picture', '770x300', adapt_rotation=False, verbose_name='Beskjæring', size_warning=False, allow_fullsize=False, help_text=None, free_crop=False, hide_image_field=False)),
                ('slug', models.SlugField(blank=True, help_text='Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres', null=True)),
                ('allow_comments', models.BooleanField(help_text='Hvorvidt kommentering er tillatt', verbose_name='Tillat kommentarer', default=True)),
                ('headline', models.CharField(max_length=100, verbose_name='tittel')),
                ('lead_paragraph', models.TextField(blank=True, help_text='Vises på forsiden og i artikkelen', verbose_name='ingress')),
                ('body', models.TextField(blank=True, help_text='Vises kun i artikkelen. Man kan her bruke <a href="http://en.wikipedia.org/wiki/Markdown" target="_blank">markdown</a> for å formatere teksten.', verbose_name='brødtekst')),
                ('priority', models.IntegerField(choices=[(0, '0 - Dukker ikke opp'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10 - Er på forsida hele tiden')], help_text='Prioritering av saken på forsiden. Dette fungerer for øyeblikket ikke. Bortsett fra at prioritering=0 fjerner saken fra forsiden.', verbose_name='Prioritering', default=5)),
                ('created_by', models.ForeignKey(related_name='news_created', editable=False, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Opprettet av', null=True)),
                ('last_changed_by', models.ForeignKey(related_name='news_edited', editable=False, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Endret av', null=True)),
                ('view_counter', models.IntegerField(editable=False, verbose_name='Visninger', default=0)),
                ('publication_date', models.DateTimeField(blank=True, verbose_name='Publikasjonstid', null=True)),
                ('published', models.NullBooleanField(help_text='Dato har høyere prioritet enn dette feltet.', verbose_name='Publisert', default=True)),
                ('content_type', models.ForeignKey(editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'verbose_name': 'nyhet',
                'verbose_name_plural': 'nyheter',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('news_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, primary_key=True, to='content.News')),
                ('short_name', models.CharField(blank=True, help_text='Brukes på steder hvor det ikke er plass til å skrive hele overskriften, for eksempel kalenderen.', max_length=20, null=True, verbose_name='kort navn')),
                ('organizer', models.CharField(blank=True, help_text='Den som står bak arrangementet', max_length=100, verbose_name='organisert av')),
                ('location', models.CharField(max_length=100, verbose_name='sted')),
                ('event_start', models.DateTimeField(verbose_name='start', null=True)),
                ('event_end', models.DateTimeField(blank=True, verbose_name='slutt', null=True)),
                ('facebook_url', models.CharField(blank=True, help_text='URL-en til det tilsvarende arrangementet på Facebook', max_length=100, verbose_name='facebook-url')),
                ('registration_required', models.BooleanField(verbose_name='påmelding', default=False)),
                ('registration_deadline', models.DateTimeField(blank=True, verbose_name='påmeldingsfrist', null=True)),
                ('registration_start', models.DateTimeField(blank=True, verbose_name='påmelding åpner', null=True)),
                ('deregistration_deadline', models.DateTimeField(blank=True, verbose_name='avmeldingsfrist', null=True)),
                ('places', models.PositiveIntegerField(blank=True, verbose_name='antall plasser', null=True)),
                ('has_queue', models.NullBooleanField(help_text='Om ventelisten er på, vil det være mulig å melde seg på selv om arrangementet er fullt. De som er i ventelisten vil automatisk bli påmeldt etter hvert som plasser blir ledige.', verbose_name='har venteliste')),
                ('open_for', models.ManyToManyField(blank=True, help_text='Hvilke grupper som får lov til å melde seg på arrangementet. Hvis ingen grupper er valgt er det åpent for alle.', to='auth.Group', verbose_name='Åpen for')),
            ],
            options={
                'permissions': (('administer', 'Can administer events'),),
                'verbose_name': 'arrangement',
                'verbose_name_plural': 'arrangement',
            },
            bases=('content.news', models.Model),
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
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=80, verbose_name='Navn')),
                ('description', models.TextField(blank=True, verbose_name='Beskrivelse')),
            ],
        ),
        migrations.CreateModel(
            name='ArchiveEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(blank=True, max_length=80, verbose_name='Tittel')),
                ('pub_date', models.DateField(help_text='Publikasjonsdato', verbose_name='publisert', null=True)),
                ('file', models.FileField(help_text='Filnavn', verbose_name='Fil', upload_to='archive')),
                ('archive', models.ForeignKey(related_name='archive', to='content.Archive', verbose_name='Arkiv')),
            ],
            options={
                'ordering': ('-pub_date',),
                'verbose_name': 'Arkivinnlegg',
                'verbose_name_plural': 'Arkivinnlegg',
            },
        ),
        migrations.AddField(
            model_name='archive',
            name='entries',
            field=models.ManyToManyField(blank=True, related_name='entries', to='content.ArchiveEntry', verbose_name='Innlegg'),
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateField(verbose_name='Opprettet', auto_created=True)),
                ('name', models.CharField(max_length=80, verbose_name='Navn')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Blogg',
                'verbose_name_plural': 'Blogger',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Publiseringsdato', null=True)),
                ('last_changed_date', models.DateTimeField(verbose_name='Redigeringsdato', null=True, auto_now=True)),
                ('title', models.CharField(max_length=80, verbose_name='Tittel')),
                ('content', models.TextField(help_text='Her kan du skrive i Markdown', verbose_name='Innhold')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('allow_comments', models.BooleanField(help_text='Hvorvidt kommentering er tillatt', verbose_name='Tillat kommentarer', default=True)),
                ('blog', models.ForeignKey(related_name='posts', to='content.Blog', verbose_name='Blogg')),
                ('created_by', models.ForeignKey(related_name='blogpost_created', editable=False, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Opprettet av', null=True)),
                ('last_changed_by', models.ForeignKey(related_name='blogpost_edited', editable=False, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Endret av', null=True)),
                ('view_counter', models.IntegerField(editable=False, verbose_name='Visninger', default=0)),
                ('list_image', models.ImageField(upload_to='blogpics', blank=True, help_text='Bilde som vises i listevisningen av bloggene', verbose_name='Listebilde', null=True)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Poster',
            },
        ),
        migrations.CreateModel(
            name='ContentImage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('file', models.ImageField(verbose_name='Bildefil', upload_to='uploads/content')),
            ],
            options={
                'verbose_name': 'Innholdsbilde',
                'verbose_name_plural': 'Innholdsbilder'
            },
        ),
        migrations.CreateModel(
            name='SplashConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(verbose_name='Enabled', default=False)),
                ('cookie_name', models.TextField(help_text='The name of the cookie to check when assessing if the user needs to be redirected', default='splash_screen')),
                ('cookie_allowed_values', models.TextField(help_text='Comma-separated list of values accepted as cookie values to prevent the redirect', default='seen')),
                ('unaffected_usernames', models.TextField(blank=True, help_text='Comma-separated list of users which should never be redirected (usernames)', default='')),
                ('unaffected_url_paths', models.TextField(blank=True, help_text='Comma-separated list of URL paths (not including the hostname) which should not be redirected. Paths may include wildcards denoted by * (example: /*/student_view)', default='')),
                ('redirect_url', models.URLField(help_text="The URL the users should be redirected to when they don't have the right cookie", default='https://example.com')),
                ('changed_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, editable=False, to=settings.AUTH_USER_MODEL, verbose_name='Changed by', null=True)),
            ],
            options={
                'abstract': False,
                'ordering': ('-change_date',),
            },
        ),
    ]
