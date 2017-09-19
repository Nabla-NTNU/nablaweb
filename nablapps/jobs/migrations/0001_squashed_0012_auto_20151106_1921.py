# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import image_cropping.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_date', models.DateTimeField(verbose_name='Publiseringsdato', auto_now_add=True, null=True)),
                ('last_changed_date', models.DateTimeField(verbose_name='Redigeringsdato', null=True, auto_now=True)),
                ('picture', models.ImageField(verbose_name='Bilde', help_text='Bilder som er større enn 770x300 px ser best ut. Du kan beskjære bildet etter opplasting.', blank=True, upload_to='uploads/news_pictures', null=True)),
                ('cropping', image_cropping.fields.ImageRatioField('picture', '770x300', hide_image_field=False, adapt_rotation=False, help_text=None, verbose_name='Beskjæring', allow_fullsize=False, size_warning=False, free_crop=False)),
                ('slug', models.SlugField(help_text='Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres', blank=True, null=True)),
                ('website', models.URLField(verbose_name='Nettside', blank=True)),
                ('name', models.CharField(verbose_name='navn', max_length=200)),
                ('description', models.TextField(verbose_name='beskrivelse', blank=True)),
                ('created_by', models.ForeignKey(related_name='company_created', to=settings.AUTH_USER_MODEL, verbose_name='Opprettet av', blank=True, null=True, editable=False)),
                ('last_changed_by', models.ForeignKey(related_name='company_edited', to=settings.AUTH_USER_MODEL, verbose_name='Endret av', blank=True, null=True, editable=False)),
                ('edit_listeners', models.ManyToManyField(help_text='Brukere som overvåker dette objektet', blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Lyttere')),
                ('view_counter', models.IntegerField(verbose_name='Visninger', default=0, editable=False)),
                ('publication_date', models.DateTimeField(verbose_name='Publikasjonstid', blank=True, null=True)),
                ('published', models.NullBooleanField(help_text='Dato har høyere prioritet enn dette feltet.', default=True, verbose_name='Publisert')),
                ('allow_comments', models.BooleanField(help_text='Hvorvidt kommentering er tillatt', default=True, verbose_name='Tillat kommentarer')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', editable=False, null=True)),
            ],
            options={
                'verbose_name_plural': 'bedrifter',
                'verbose_name': 'bedrift',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='RelevantForChoices',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('studieretning', models.CharField(help_text='Mulige valg for "relevant for" når man legger til stillingsannonser.', max_length=50, verbose_name='Valg')),
            ],
            options={
                'verbose_name_plural': 'Mulige valg for "relevant for"',
                'verbose_name': 'Mulig valg for "relevant for"',
            },
        ),
        migrations.CreateModel(
            name='TagChoices',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('tag', models.CharField(help_text='Tags for stillingsannonsen. Eksempler: deltid, sommerjobb, fulltid, utlandet, by. Søkbar.', max_length=100, verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'verbose_name': 'Tag',
                'ordering': ('tag',),
            },
        ),
        migrations.CreateModel(
            name='YearChoices',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('year', models.IntegerField(help_text='Klasse: 1, 2, 3, 4 og 5', verbose_name='Klasse')),
            ],
            options={
                'verbose_name_plural': 'Klasser',
                'verbose_name': 'Klasse',
                'permissions': (('can_see_static_models', 'Can see static models'),),
            },
        ),
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('news_ptr', models.OneToOneField(auto_created=True, parent_link=True, primary_key=True, serialize=False, to='news.News')),
                ('deadline_date', models.DateTimeField(help_text='Søknadsfrist', blank=True, null=True, verbose_name='Frist')),
                ('removal_date', models.DateTimeField(help_text='Når annonsen fjernes fra listen, f.eks. samtidig som søknadsfristen', verbose_name='Forsvinner')),
                ('info_file', models.FileField(help_text='Informasjon om stillingen', blank=True, upload_to='stillinger', verbose_name='Informasjonsfil')),
                ('info_website', models.URLField(help_text='Nettside der man kan søke på stillingen eller få mer informasjon', blank=True, max_length=150, verbose_name='Infoside')),
                ('company', models.ForeignKey(verbose_name='Bedrift', help_text='Hvilken bedrift stillingen er hos', to='jobs.Company')),
                ('relevant_for_group', models.ManyToManyField(help_text='Hvilke studieretninger stillingsannonsen er relevant for.', to='jobs.RelevantForChoices', verbose_name='Studieretning')),
                ('relevant_for_year', models.ManyToManyField(help_text='Hvilke årskull stillingsannonsen er relevant for.', to='jobs.YearChoices', verbose_name='Årskull')),
                ('tags', models.ManyToManyField(verbose_name='Tags', blank=True, help_text='F.eks. sommerjobb, bergen, kirkenes, olje, konsultering...', to='jobs.TagChoices')),
            ],
            options={'verbose_name_plural': 'stillingsannonser', 'verbose_name': 'stillingsannonse', 'ordering': ('-created_date', 'headline')},
            bases=('news.news',),
        ),
    ]
