# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('news_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.News')),
                ('deadline_date', models.DateTimeField(help_text='Søknadsfrist', null=True, verbose_name='Frist', blank=True)),
                ('removal_date', models.DateTimeField(help_text='Når annonsen fjernes fra listen, f.eks. samtidig som søknadsfristen', verbose_name='Forsvinner')),
                ('info_file', models.FileField(help_text='Informasjon om stillingen', upload_to='stillinger', verbose_name='Informasjonsfil', blank=True)),
                ('info_website', models.URLField(help_text='Nettside der man kan søke på stillingen eller få mer informasjon', max_length=150, verbose_name='Infoside', blank=True)),
            ],
            options={
                'verbose_name': 'stillingsannonse',
                'verbose_name_plural': 'stillingsannonser',
            },
            bases=('content.news',),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Publiseringsdato', null=True)),
                ('last_changed_date', models.DateTimeField(auto_now=True, verbose_name='Redigeringsdato', null=True)),
                ('picture', models.ImageField(help_text='Bilder som er større enn 770x300 px ser best ut. Du kan beskjære bildet etter opplasting.', upload_to='news_pictures', null=True, verbose_name='Bilde', blank=True)),
                ('cropping', image_cropping.fields.ImageRatioField('picture', '770x300', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='Beskjæring')),
                ('slug', models.SlugField(help_text='Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres', null=True, blank=True)),
                ('allow_comments', models.BooleanField(default=True, help_text='Hvorvidt kommentering er tillatt', verbose_name='Tillat kommentarer')),
                ('website', models.URLField(verbose_name='Nettside', blank=True)),
                ('name', models.CharField(max_length=200, verbose_name='navn')),
                ('description', models.TextField(verbose_name='beskrivelse', blank=True)),
                ('content_type', models.ForeignKey(editable=False, to='contenttypes.ContentType', null=True)),
                ('created_by', models.ForeignKey(related_name='company_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Opprettet av')),
                ('last_changed_by', models.ForeignKey(related_name='company_edited', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Endret av')),
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
                ('studieretning', models.CharField(help_text='Mulige valg for "relevant for" når man legger til stillingsannonser.', max_length=50, verbose_name='Valg')),
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
                ('tag', models.CharField(help_text='Tags for stillingsannonsen. Eksempler: deltid, sommerjobb, fulltid, utlandet, by. Søkbar.', max_length=100, verbose_name='Tags')),
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
                ('year', models.IntegerField(help_text='Klasse: 1, 2, 3, 4 og 5', verbose_name='Klasse')),
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
            field=models.ForeignKey(verbose_name='Bedrift', to='jobs.Company', help_text='Hvilken bedrift stillingen er hos'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advert',
            name='relevant_for_group',
            field=models.ManyToManyField(help_text='Hvilke studieretninger stillingsannonsen er relevant for.', to='jobs.RelevantForChoices', verbose_name='Studieretning'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advert',
            name='relevant_for_year',
            field=models.ManyToManyField(help_text='Hvilke årskull stillingsannonsen er relevant for.', to='jobs.YearChoices', null=True, verbose_name='årskull'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advert',
            name='tags',
            field=models.ManyToManyField(help_text='F.eks. sommerjobb, bergen, kirkenes, olje, konsultering...', to='jobs.TagChoices', verbose_name='Tags', blank=True),
            preserve_default=True,
        ),
    ]
