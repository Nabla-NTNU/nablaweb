# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interactive', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionReply',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('alternative', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('view_counter', models.IntegerField(editable=False, default=0, verbose_name='Visninger')),
                ('created_date', models.DateTimeField(null=True, auto_now_add=True, verbose_name='Publiseringsdato')),
                ('last_changed_date', models.DateTimeField(null=True, auto_now=True, verbose_name='Redigeringsdato')),
                ('template', models.CharField(max_length=100, verbose_name='Template', default='interactive/advent_door_base.html')),
                ('title', models.CharField(max_length=80, verbose_name='Tittel')),
                ('is_timed', models.BooleanField(verbose_name='Bruk tidsbegrensning?', default=False)),
                ('duration', models.PositiveIntegerField(verbose_name='Tidsbegrensning', null=True, blank=True)),
                ('created_by', models.ForeignKey(editable=False, null=True, to=settings.AUTH_USER_MODEL, verbose_name='Opprettet av', blank=True, related_name='quiz_created')),
                ('edit_listeners', models.ManyToManyField(help_text='Brukere som overvåker dette objektet', verbose_name='Lyttere', blank=True, to=settings.AUTH_USER_MODEL)),
                ('last_changed_by', models.ForeignKey(editable=False, null=True, to=settings.AUTH_USER_MODEL, verbose_name='Endret av', blank=True, related_name='quiz_edited')),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizer',
            },
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('question', models.CharField(max_length=200, verbose_name='Spørsmål')),
                ('correct_alternative', models.IntegerField(verbose_name='Riktig svar', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')])),
                ('alternative_1', models.CharField(max_length=200, verbose_name='Alternativ 1')),
                ('alternative_2', models.CharField(max_length=200, verbose_name='Alternativ 2')),
                ('alternative_3', models.CharField(max_length=200, verbose_name='Alternativ 3')),
                ('alternative_4', models.CharField(max_length=200, verbose_name='Alternativ 4')),
                ('quiz', models.ForeignKey(related_name='questions', to='interactive.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='QuizReply',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
            ],
            options={
                'verbose_name': 'Resultat',
                'verbose_name_plural': 'Resultater',
            },
        ),
        migrations.CreateModel(
            name='QuizScoreboard',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='quizreply',
            name='scoreboard',
            field=models.ForeignKey(related_name='replies', to='interactive.QuizScoreboard'),
        ),
        migrations.AddField(
            model_name='quizreply',
            name='user',
            field=models.ForeignKey(related_name='interaction_results', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quiz',
            name='scoreboard',
            field=models.OneToOneField(null=True, to='interactive.QuizScoreboard', related_name='quiz'),
        ),
        migrations.AddField(
            model_name='questionreply',
            name='question',
            field=models.ForeignKey(to='interactive.QuizQuestion'),
        ),
        migrations.AddField(
            model_name='questionreply',
            name='quiz_reply',
            field=models.ForeignKey(null=True, to='interactive.QuizReply', related_name='questions'),
        ),
    ]
