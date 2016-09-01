# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('link_info', models.CharField(max_length=120, verbose_name='link info', help_text='Link info')),
                ('linken', models.TextField(verbose_name='linken', help_text='Linken')),
                ('univ_navn', models.CharField(max_length=30, verbose_name='Universitet')),
            ],
            options={
                'ordering': ('link_info',),
            },
        ),
        migrations.CreateModel(
            name='Universitet',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('univ_navn', models.CharField(max_length=30, verbose_name='universitets navn', help_text='Universitets navn', default='')),
                ('land', models.TextField(verbose_name='land', help_text='Land', default='')),
            ],
            options={
                'ordering': ('univ_navn',),
            },
        ),
        migrations.CreateModel(
            name='Utveksling',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('student_navn', models.CharField(max_length=30, verbose_name='student_navn', help_text='Student navn')),
                ('retning', models.CharField(max_length=30, choices=[('biofys', 'Biofysikk og medisinteknologi'), ('indmat', 'Industriell matematikk'), ('tekfys', 'Teknisk fysikk')], help_text='Retning')),
                ('epost', models.CharField(max_length=50, default='', help_text='E-post')),
                ('ex_year', models.IntegerField(verbose_name='Arstall')),
                ('univ_navn', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ('student_navn',),
            },
        ),
    ]
