# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    replaces = [('podcast', '0001_initial'), ('podcast', '0002_auto_20150214_2044'), ('podcast', '0003_auto_20150521_0025'), ('podcast', '0004_auto_20150525_1806'), ('podcast', '0005_auto_20150727_2133'), ('podcast', '0006_auto_20150727_2135'), ('podcast', '0007_auto_20150727_2210'), ('podcast', '0008_season_logo'), ('podcast', '0009_auto_20150808_1725'), ('podcast', '0010_auto_20150810_1206'), ('podcast', '0011_auto_20151102_2035'), ('podcast', '0012_auto_20151103_0013'), ('podcast', '0013_podcast_allow_comments'), ('podcast', '0014_podcast_content_type')]

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('number', models.IntegerField(unique=True, verbose_name='Sesongnummer')),
                ('banner', models.ImageField(help_text='Sesongbanner.', null=True, upload_to='podcast/images', verbose_name='Banner', blank=True)),
                ('logo', models.ImageField(help_text='Podcastlogo.', null=True, upload_to='podcast/images', verbose_name='Logo', blank=True)),
            ],
            options={'verbose_name_plural': 'Sesonger', 'verbose_name': 'Sesong'},
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(verbose_name='tittel', max_length=200)),
                ('description', models.TextField(verbose_name='beskrivelse', help_text='Teksten vil bli kuttet etter 250 tegn på sesongsiden.', blank=True)),
                ('pub_date', models.DateTimeField(verbose_name='publisert', null=True)),
                ('file', models.FileField(upload_to='podcast', verbose_name='lydfil', help_text='Filformat: MP3', blank=True)),
                ('view_counter', models.IntegerField(verbose_name='Visninger', editable=False, default=0)),
                ('cropping', image_cropping.fields.ImageRatioField('image', '300x300', allow_fullsize=False, adapt_rotation=False, size_warning=False, help_text='Bildet vises i full form på detaljsiden.', free_crop=False, verbose_name='Beskjæring', hide_image_field=False)),
                ('image', models.ImageField(help_text='Bilder som er større enn 300x300 px ser best ut. Du kan beskjære bildet etter opplasting.', null=True, upload_to='news_pictures', verbose_name='Bilde', blank=True)),
                ('is_clip', models.BooleanField(verbose_name='Er lydklipp', help_text='Lydklipp blir ikke vist sammen med episodene.', default=False)),
                ('season', models.ForeignKey(to='podcast.Season', null=True, verbose_name='Sesong', blank=True, on_delete=models.CASCADE)),
                ('extra_markdown', models.TextField(verbose_name='Ekstra markdown', help_text='Ekstra markdown for å putte inn videoer etc.', null=True, blank=True)),
                ('publication_date', models.DateTimeField(verbose_name='Publikasjonstid', null=True, blank=True)),
                ('published', models.NullBooleanField(verbose_name='Publisert', help_text='Dato har høyere prioritet enn dette feltet.', default=True)),
                ('allow_comments', models.BooleanField(verbose_name='Tillat kommentarer', help_text='Hvorvidt kommentering er tillatt', default=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True, editable=False, on_delete=models.CASCADE)),
            ],
            options={'verbose_name_plural': 'Podcast', 'verbose_name': 'Podcast', 'ordering': ['-pub_date']},
        ),
    ]
