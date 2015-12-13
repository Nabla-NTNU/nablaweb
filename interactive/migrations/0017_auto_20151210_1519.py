# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interactive', '0016_auto_20151130_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('view_counter', models.IntegerField(default=0, verbose_name='Visninger', editable=False)),
                ('created_date', models.DateTimeField(null=True, verbose_name='Publiseringsdato', auto_now_add=True)),
                ('last_changed_date', models.DateTimeField(null=True, verbose_name='Redigeringsdato', auto_now=True)),
                ('template', models.CharField(max_length=100, default='interactive/advent_door_base.html', verbose_name='Template')),
                ('created_by', models.ForeignKey(null=True, related_name='test_created', blank=True, editable=False, verbose_name='Opprettet av', to=settings.AUTH_USER_MODEL)),
                ('edit_listeners', models.ManyToManyField(verbose_name='Lyttere', to=settings.AUTH_USER_MODEL, help_text='Brukere som overvåker dette objektet', blank=True)),
                ('last_changed_by', models.ForeignKey(null=True, related_name='test_edited', blank=True, editable=False, verbose_name='Endret av', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestQuestion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TestQuestionAlternative',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='testquestion',
            name='alternatives',
            field=models.ManyToManyField(to='interactive.TestQuestionAlternative'),
        ),
        migrations.AddField(
            model_name='test',
            name='questions',
            field=models.ManyToManyField(to='interactive.TestQuestion'),
        ),
        migrations.AddField(
            model_name='test',
            name='results',
            field=models.ManyToManyField(to='interactive.TestResult'),
        ),
    ]
