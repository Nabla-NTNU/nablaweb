# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('retning', models.CharField(help_text='Retning', choices=[('Biofysikk og medisinteknologi', 'biofys'), ('Industriell matematikk', 'indmat'), ('Teknisk fysikk', 'tekfys')], max_length=30)),
                ('start', models.DateField(help_text='Dato utveksling startet')),
                ('end', models.DateField(help_text='Dato utveksling sluttet')),
                ('student', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['student'],
            },
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(help_text='Tittelen til innholdet', default='', max_length=50, verbose_name='tittel')),
                ('body', models.TextField(help_text='Man kan her bruke <a href="http://en.wikipedia.org/wiki/Markdown" target="_blank">markdown</a> for å formatere teksten.', verbose_name='brødtekst', blank=True)),
                ('ex', models.ForeignKey(to='exchange.Exchange')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('univ_navn', models.CharField(help_text='Navnet til universitetet', default='', max_length=50, verbose_name='universitets navn')),
                ('land', models.CharField(help_text='Landet universitetet ligger i', default='', max_length=30, verbose_name='land')),
            ],
            options={
                'ordering': ['univ_navn'],
            },
        ),
        migrations.AddField(
            model_name='exchange',
            name='univ',
            field=models.ForeignKey(to='exchange.University'),
        ),
    ]
