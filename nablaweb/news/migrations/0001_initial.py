# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Publiseringsdato', null=True)),
                ('last_changed_date', models.DateTimeField(auto_now=True, verbose_name='Redigeringsdato', null=True)),
                ('picture', models.ImageField(help_text='Bilder som er større enn 770x300 px ser best ut. Du kan beskjære bildet etter opplasting.', upload_to='news_pictures', null=True, verbose_name='Bilde', blank=True)),
                ('cropping', image_cropping.fields.ImageRatioField('picture', '770x300', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='Beskjæring')),
                ('slug', models.SlugField(help_text='Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres', null=True, blank=True)),
                ('allow_comments', models.BooleanField(default=True, help_text='Hvorvidt kommentering er tillatt', verbose_name='Tillat kommentarer')),
                ('headline', models.CharField(max_length=100, verbose_name='tittel')),
                ('lead_paragraph', models.TextField(help_text='Vises på forsiden og i artikkelen', verbose_name='ingress', blank=True)),
                ('body', models.TextField(help_text='Vises kun i artikkelen. Man kan her bruke <a href="http://en.wikipedia.org/wiki/Markdown" target="_blank">markdown</a> for å formatere teksten.', verbose_name='brødtekst', blank=True)),
                ('priority', models.IntegerField(default=5, help_text='Prioritering av saken på forsiden. Dette fungerer for øyeblikket ikke. Bortsett fra at prioritering=0 fjerner saken fra forsiden.', verbose_name='Prioritering', choices=[(0, '0 - Dukker ikke opp'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10 - Er på forsida hele tiden')])),
                ('content_type', models.ForeignKey(editable=False, to='contenttypes.ContentType', null=True)),
                ('created_by', models.ForeignKey(related_name='news_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Opprettet av')),
                ('last_changed_by', models.ForeignKey(related_name='news_edited', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Endret av')),
            ],
            options={
                'verbose_name': 'nyhet',
                'verbose_name_plural': 'nyheter',
            },
            bases=(models.Model,),
        ),
    ]
