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
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name=b'Publiseringsdato', null=True)),
                ('last_changed_date', models.DateTimeField(auto_now=True, verbose_name=b'Redigeringsdato', null=True)),
                ('picture', models.ImageField(help_text=b'Bilder som er st\xc3\xb8rre enn 770x300 px ser best ut. Du kan beskj\xc3\xa6re bildet etter opplasting.', upload_to=b'news_pictures', null=True, verbose_name=b'Bilde', blank=True)),
                (b'cropping', image_cropping.fields.ImageRatioField(b'picture', '770x300', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name=b'Beskj\xc3\xa6ring')),
                ('slug', models.SlugField(help_text=b'Denne teksten vises i adressen til siden, og trengs vanligvis ikke \xc3\xa5 endres', null=True, blank=True)),
                ('allow_comments', models.BooleanField(default=True, help_text=b'Hvorvidt kommentering er tillatt', verbose_name=b'Tillat kommentarer')),
                ('headline', models.CharField(max_length=100, verbose_name=b'tittel')),
                ('lead_paragraph', models.TextField(help_text=b'Vises p\xc3\xa5 forsiden og i artikkelen', verbose_name=b'ingress', blank=True)),
                ('body', models.TextField(help_text=b'Vises kun i artikkelen. Man kan her bruke <a href="http://en.wikipedia.org/wiki/Markdown" target="_blank">markdown</a> for \xc3\xa5 formatere teksten.', verbose_name=b'br\xc3\xb8dtekst', blank=True)),
                ('priority', models.IntegerField(default=5, help_text=b'Prioritering av saken p\xc3\xa5 forsiden. Dette fungerer for \xc3\xb8yeblikket ikke. Bortsett fra at prioritering=0 fjerner saken fra forsiden.', verbose_name=b'Prioritering', choices=[(0, b'0 - Dukker ikke opp'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9'), (10, b'10 - Er p\xc3\xa5 forsida hele tiden')])),
                ('content_type', models.ForeignKey(editable=False, to='contenttypes.ContentType', null=True)),
                ('created_by', models.ForeignKey(related_name=b'news_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Opprettet av')),
                ('last_changed_by', models.ForeignKey(related_name=b'news_edited', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Endret av')),
            ],
            options={
                'verbose_name': 'nyhet',
                'verbose_name_plural': 'nyheter',
            },
            bases=(models.Model,),
        ),
    ]
