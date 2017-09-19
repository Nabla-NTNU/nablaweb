# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
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
    ]
