# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20150812_0721'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Navn', max_length=80)),
                ('description', models.TextField(verbose_name='Beskrivelse', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ArchiveEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(blank=True, verbose_name='Tittel', max_length=80)),
                ('pub_date', models.DateField(verbose_name='publisert', help_text='Publikasjonsdato', null=True)),
                ('file', models.FileField(verbose_name='Fil', help_text='Filnavn', upload_to='archive')),
                ('archive', models.ForeignKey(to='content.Archive', related_name='archive', verbose_name='Arkiv')),
            ],
            options={
                'ordering': ('-pub_date',),
                'verbose_name': 'Arkivinnlegg',
                'verbose_name_plural': 'Arkivinnlegg',
            },
        ),
        migrations.AlterField(
            model_name='albumimage',
            name='file',
            field=models.FileField(verbose_name='Bildefil', upload_to=''),
        ),
        migrations.AddField(
            model_name='archive',
            name='entries',
            field=models.ManyToManyField(to='content.ArchiveEntry', verbose_name='Innlegg', related_name='entries', blank=True),
        ),
    ]
