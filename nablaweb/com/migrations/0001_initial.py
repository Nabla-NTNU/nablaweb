# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ComMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('story', models.TextField(help_text=b'Ansvarsomr\xc3\xa5de eller lignende', verbose_name=b'Beskrivelse', blank=True)),
                ('joined_date', models.DateField(help_text=b'Dato personen ble med i komiteen', null=True, verbose_name=b'Ble med', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name=b'Aktiv?')),
                ('com', models.ForeignKey(verbose_name=b'Komit\xc3\xa9', to='auth.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'komitemedlem',
                'verbose_name_plural': 'komitemedlemmer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ComPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(help_text=b'Teksten p\xc3\xa5 komit\xc3\xa9siden', verbose_name=b'Beskrivelse', blank=True)),
                ('slug', models.CharField(verbose_name=b'Slug til URL-er', unique=True, max_length=50, editable=False)),
                ('last_changed_date', models.DateTimeField(auto_now=True, verbose_name=b'Sist redigert', null=True)),
                ('com', models.ForeignKey(to='auth.Group')),
                ('last_changed_by', models.ForeignKey(related_name=b'compage_edited', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Sist endret av')),
            ],
            options={
                'verbose_name': 'komiteside',
                'verbose_name_plural': 'komitesider',
            },
            bases=(models.Model,),
        ),
    ]
