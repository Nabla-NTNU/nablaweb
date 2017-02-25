# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import interactive.models.user_test
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('interactive', '0001_initial'), ('interactive', '0002_auto_20151016_1758'), ('interactive', '0003_quizreply_when'), ('interactive', '0004_quizreply_score'), ('interactive', '0005_adventdoor_is_lottery'), ('interactive', '0006_adventdoor_participating_users'), ('interactive', '0007_adventdoor_short_description'), ('interactive', '0008_auto_20151104_0131'), ('interactive', '0009_adventdoor_content_type'), ('interactive', '0010_auto_20151108_1501'), ('interactive', '0011_quiz_content_type'), ('interactive', '0012_auto_20151110_2156'), ('interactive', '0013_adventdoor_is_text_response'), ('interactive', '0014_adventdoor_image'), ('interactive', '0015_adventdoor_quiz'), ('interactive', '0016_auto_20151130_1056'), ('interactive', '0017_auto_20151210_1519'), ('interactive', '0018_auto_20151212_2135'), ('interactive', '0019_auto_20160402_1630'), ('interactive', '0020_auto_20161102_1946'), ('interactive', '0021_auto_20161118_0407'), ('interactive', '0022_adventdoor_user_test')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('com', '0003_auto_20151007_1436'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizScoreboard',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('view_counter', models.IntegerField(editable=False, verbose_name='Visninger', default=0)),
                ('created_date', models.DateTimeField(null=True, verbose_name='Publiseringsdato', auto_now_add=True)),
                ('last_changed_date', models.DateTimeField(null=True, auto_now=True, verbose_name='Redigeringsdato')),
                ('template', models.CharField(max_length=100, verbose_name='Template', default='interactive/advent_door_base.html')),
                ('title', models.CharField(max_length=80, verbose_name='Tittel')),
                ('is_timed', models.BooleanField(verbose_name='Bruk tidsbegrensning?', default=False)),
                ('duration', models.PositiveIntegerField(null=True, verbose_name='Tidsbegrensning', help_text='Tid til å fullføre quizen målt i sekunder.', blank=True)),
                ('created_by', models.ForeignKey(null=True, editable=False, blank=True, verbose_name='Opprettet av', to=settings.AUTH_USER_MODEL, related_name='quiz_created')),
                ('edit_listeners', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Lyttere', help_text='Brukere som overvåker dette objektet', blank=True)),
                ('last_changed_by', models.ForeignKey(null=True, editable=False, blank=True, verbose_name='Endret av', to=settings.AUTH_USER_MODEL, related_name='quiz_edited')),
                ('scoreboard', models.OneToOneField(null=True, to='interactive.QuizScoreboard', related_name='quiz')),
                ('publication_date', models.DateTimeField(null=True, verbose_name='Publikasjonstid', blank=True)),
                ('published', models.NullBooleanField(verbose_name='Publisert', help_text='Dato har høyere prioritet enn dette feltet.', default=True)),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizer',
            },
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('question', models.TextField(verbose_name='Spørsmål')),
                ('correct_alternative', models.IntegerField(verbose_name='Riktig svar', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')])),
                ('alternative_1', models.CharField(max_length=200, verbose_name='Alternativ 1')),
                ('alternative_2', models.CharField(max_length=200, verbose_name='Alternativ 2')),
                ('alternative_3', models.CharField(max_length=200, verbose_name='Alternativ 3')),
                ('alternative_4', models.CharField(max_length=200, verbose_name='Alternativ 4')),
                ('quiz', models.ForeignKey(to='interactive.Quiz', related_name='questions')),
            ],
        ),
        migrations.CreateModel(
            name='QuizReply',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('scoreboard', models.ForeignKey(to='interactive.QuizScoreboard', related_name='replies')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='interaction_results')),
                ('when', models.DateTimeField(auto_created=True)),
                ('score', models.IntegerField(null=True, blank=True)),
                ('start', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Resultat',
                'verbose_name_plural': 'Resultater',
            },
        ),
        migrations.CreateModel(
            name='QuestionReply',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('alternative', models.PositiveIntegerField()),
                ('question', models.ForeignKey(to='interactive.QuizQuestion')),
                ('quiz_reply', models.ForeignKey(null=True, to='interactive.QuizReply', related_name='questions')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('view_counter', models.IntegerField(editable=False, verbose_name='Visninger', default=0)),
                ('created_date', models.DateTimeField(null=True, verbose_name='Publiseringsdato', auto_now_add=True)),
                ('last_changed_date', models.DateTimeField(null=True, auto_now=True, verbose_name='Redigeringsdato')),
                ('template', models.CharField(max_length=100, verbose_name='Template', default='interactive/advent_door_base.html')),
                ('created_by', models.ForeignKey(null=True, editable=False, blank=True, verbose_name='Opprettet av', to=settings.AUTH_USER_MODEL, related_name='test_created')),
                ('edit_listeners', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Lyttere', help_text='Brukere som overvåker dette objektet', blank=True)),
                ('last_changed_by', models.ForeignKey(null=True, editable=False, blank=True, verbose_name='Endret av', to=settings.AUTH_USER_MODEL, related_name='test_edited')),
                ('publication_date', models.DateTimeField(null=True, verbose_name='Publikasjonstid', blank=True)),
                ('published', models.NullBooleanField(verbose_name='Publisert', help_text='Dato har høyere prioritet enn dette feltet.', default=True)),
                ('title', models.TextField(verbose_name='tittel', help_text='Tittel på brukertesten', default='')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'brukertest',
                'verbose_name_plural': 'brukertester',
            },
        ),
        migrations.CreateModel(
            name='TestQuestion',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('text', models.TextField(verbose_name='spørsmål', default='')),
                ('test', models.ForeignKey(null=True, to='interactive.Test', related_name='questions')),
            ],
            options={
                'verbose_name': 'testspørsmål',
                'verbose_name_plural': 'testspørsmål'
            },
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(verbose_name='beskrivelse')),
                ('test', models.ForeignKey(null=True, to='interactive.Test', related_name='results')),
            ],
            options={'verbose_name': 'testresultat', 'verbose_name_plural': 'testresultater'},
        ),
        migrations.CreateModel(
            name='TestQuestionAlternative',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('text', models.TextField(verbose_name='svaralternativ')),
                ('weights', models.TextField(help_text='Bestem hvor mye hvert resultat vektlegges ved valg av dette alternativet. Format er 3,1,4 (altså heltall) det 3 er vekten til det øveste resultatet osv. Hvis blank får alle vekt 1, og hvis listen ikke er lang nok får resten vekt 1', verbose_name='vektlegging av resultater', validators=[interactive.models.user_test.validate_weight_syntax], blank=True)),
                ('question', models.ForeignKey(null=True, to='interactive.TestQuestion', related_name='alternatives')),
                ('target', models.ManyToManyField(to='interactive.TestResult', verbose_name='tilsvarende resultat (lagre én gang for å få korrekte resultater)', help_text='Velg resultatene dette alternativet svarer til.', blank=True)),
            ],
            options={'verbose_name': 'alternativ', 'verbose_name_plural': 'alternativer'},
        ),
        migrations.CreateModel(
            name='AdventCalendar',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('year', models.IntegerField(verbose_name='År', unique=True)),
                ('template', models.CharField(max_length=100, verbose_name='Template', default='interactive/advent_base.html')),
            ],
            options={
                'verbose_name': 'Adventskalender',
                'verbose_name_plural': 'Adventskalendere',
            },
        ),
        migrations.CreateModel(
            name='AdventDoor',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('view_counter', models.IntegerField(editable=False, verbose_name='Visninger', default=0)),
                ('created_date', models.DateTimeField(null=True, verbose_name='Publiseringsdato', auto_now_add=True)),
                ('last_changed_date', models.DateTimeField(null=True, auto_now=True, verbose_name='Redigeringsdato')),
                ('template', models.CharField(max_length=100, verbose_name='Template', default='interactive/advent_door_base.html')),
                ('number', models.IntegerField(verbose_name='Nummer')),
                ('content', models.TextField(verbose_name='Innhold', blank=True)),
                ('calendar', models.ForeignKey(verbose_name='Kalender', to='interactive.AdventCalendar')),
                ('committee', models.ForeignKey(null=True, blank=True, verbose_name='Komité', to='com.Committee')),
                ('created_by', models.ForeignKey(null=True, editable=False, blank=True, verbose_name='Opprettet av', to=settings.AUTH_USER_MODEL, related_name='adventdoor_created')),
                ('edit_listeners', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Lyttere', help_text='Brukere som overvåker dette objektet', blank=True)),
                ('last_changed_by', models.ForeignKey(null=True, editable=False, blank=True, verbose_name='Endret av', to=settings.AUTH_USER_MODEL, related_name='adventdoor_edited')),
                ('winner', models.ForeignKey(null=True, blank=True, verbose_name='Vinner', to=settings.AUTH_USER_MODEL, related_name='advent_doors_won')),
                ('is_lottery', models.BooleanField(verbose_name='Har trekning', default=False)),
                ('short_description', models.CharField(null=True, max_length=200, verbose_name='Kort beskrivelse', blank=True)),
                ('is_text_response', models.BooleanField(verbose_name='Har tekstsvar', default=False)),
                ('image', models.ImageField(null=True, verbose_name='Bilde', blank=True, upload_to='')),
                ('quiz', models.ForeignKey(null=True, blank=True, verbose_name='Lenket quiz', to='interactive.Quiz')),
                ('user_test', models.ForeignKey(null=True, blank=True, verbose_name='Lenket brukertest', to='interactive.Test')),
            ],
            options={
                'verbose_name': 'Adventsluke',
                'verbose_name_plural': 'Adventsluker',
            }
        ),
        migrations.AlterUniqueTogether(
            name='adventdoor',
            unique_together=set([('number', 'calendar')]),
        ),
        migrations.CreateModel(
            name='AdventParticipation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('when', models.DateTimeField(auto_created=True)),
                ('text', models.TextField(null=True)),
                ('door', models.ForeignKey(to='interactive.AdventDoor', related_name='participation')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
