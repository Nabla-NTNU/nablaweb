# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('news_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='news.News')),
                ('deadline_date', models.DateTimeField(help_text=b'S\xc3\xb8knadsfrist', null=True, verbose_name=b'Frist', blank=True)),
                ('removal_date', models.DateTimeField(help_text=b'N\xc3\xa5r annonsen fjernes fra listen, f.eks. samtidig som s\xc3\xb8knadsfristen', verbose_name=b'Forsvinner')),
                ('info_file', models.FileField(help_text=b'Informasjon om stillingen', upload_to=b'stillinger', verbose_name=b'Informasjonsfil', blank=True)),
                ('info_website', models.URLField(help_text=b'Nettside der man kan s\xc3\xb8ke p\xc3\xa5 stillingen eller f\xc3\xa5 mer informasjon', max_length=150, verbose_name=b'Infoside', blank=True)),
            ],
            options={
                'verbose_name': 'stillingsannonse',
                'verbose_name_plural': 'stillingsannonser',
            },
            bases=('news.news',),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name=b'Publiseringsdato', null=True)),
                ('last_changed_date', models.DateTimeField(auto_now=True, verbose_name=b'Redigeringsdato', null=True)),
                ('picture', models.ImageField(help_text=b'Bilder som er st\xc3\xb8rre enn 770x300 px ser best ut. Du kan beskj\xc3\xa6re bildet etter opplasting.', upload_to=b'news_pictures', null=True, verbose_name=b'Bilde', blank=True)),
                (b'cropping', image_cropping.fields.ImageRatioField(b'picture', '770x300', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name=b'Beskj\xc3\xa6ring')),
                ('slug', models.SlugField(help_text=b'Denne teksten vises i adressen til siden, og trengs vanligvis ikke \xc3\xa5 endres', null=True, blank=True)),
                ('allow_comments', models.BooleanField(default=True, help_text=b'Hvorvidt kommentering er tillatt', verbose_name=b'Tillat kommentarer')),
                ('website', models.URLField(verbose_name=b'Nettside', blank=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'navn')),
                ('description', models.TextField(verbose_name=b'beskrivelse', blank=True)),
                ('content_type', models.ForeignKey(editable=False, to='contenttypes.ContentType', null=True)),
                ('created_by', models.ForeignKey(related_name=b'company_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Opprettet av')),
                ('last_changed_by', models.ForeignKey(related_name=b'company_edited', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Endret av')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'bedrift',
                'verbose_name_plural': 'bedrifter',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelevantForChoices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('studieretning', models.CharField(help_text=b'Mulige valg for "relevant for" n\xc3\xa5r man legger til stillingsannonser.', max_length=50, verbose_name=b'Valg')),
            ],
            options={
                'verbose_name': 'Mulig valg for "relevant for"',
                'verbose_name_plural': 'Mulige valg for "relevant for"',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagChoices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(help_text=b'Tags for stillingsannonsen. Eksempler: deltid, sommerjobb, fulltid, utlandet, by. S\xc3\xb8kbar.', max_length=100, verbose_name=b'Tags')),
            ],
            options={
                'ordering': ('tag',),
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='YearChoices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(help_text=b'Klasse: 1, 2, 3, 4 og 5', verbose_name=b'Klasse')),
            ],
            options={
                'verbose_name': 'Klasse',
                'verbose_name_plural': 'Klasser',
                'permissions': (('can_see_static_models', 'Can see static models'),),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='advert',
            name='company',
            field=models.ForeignKey(verbose_name=b'Bedrift', to='jobs.Company', help_text=b'Hvilken bedrift stillingen er hos'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advert',
            name='relevant_for_group',
            field=models.ManyToManyField(help_text=b'Hvilke studieretninger stillingsannonsen er relevant for.', to='jobs.RelevantForChoices', verbose_name=b'Studieretning'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advert',
            name='relevant_for_year',
            field=models.ManyToManyField(help_text=b'Hvilke \xc3\xa5rskull stillingsannonsen er relevant for.', to='jobs.YearChoices', null=True, verbose_name=b'\xc3\x85rskull'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advert',
            name='tags',
            field=models.ManyToManyField(help_text=b'F.eks. sommerjobb, bergen, kirkenes, olje, konsultering...', to='jobs.TagChoices', verbose_name=b'Tags', blank=True),
            preserve_default=True,
        ),
    ]
