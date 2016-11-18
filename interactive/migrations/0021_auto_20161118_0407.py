# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import interactive.models.user_test


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0020_auto_20161102_1946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='test',
            options={'verbose_name': 'brukertest', 'verbose_name_plural': 'brukertester'},
        ),
        migrations.AlterModelOptions(
            name='testquestion',
            options={'verbose_name': 'testspørsmål', 'verbose_name_plural': 'testspørsmål'},
        ),
        migrations.AlterModelOptions(
            name='testquestionalternative',
            options={'verbose_name': 'alternativ', 'verbose_name_plural': 'alternativer'},
        ),
        migrations.AlterModelOptions(
            name='testresult',
            options={'verbose_name': 'testresultat', 'verbose_name_plural': 'testresultater'},
        ),
        migrations.RemoveField(
            model_name='test',
            name='questions',
        ),
        migrations.RemoveField(
            model_name='test',
            name='results',
        ),
        migrations.RemoveField(
            model_name='testquestion',
            name='alternatives',
        ),
        migrations.AddField(
            model_name='test',
            name='publication_date',
            field=models.DateTimeField(null=True, verbose_name='Publikasjonstid', blank=True),
        ),
        migrations.AddField(
            model_name='test',
            name='published',
            field=models.NullBooleanField(default=True, help_text='Dato har høyere prioritet enn dette feltet.', verbose_name='Publisert'),
        ),
        migrations.AddField(
            model_name='test',
            name='title',
            field=models.TextField(default='', help_text='Tittel på brukertesten', verbose_name='tittel'),
        ),
        migrations.AddField(
            model_name='testquestion',
            name='test',
            field=models.ForeignKey(to='interactive.Test', null=True, related_name='questions'),
        ),
        migrations.AddField(
            model_name='testquestionalternative',
            name='question',
            field=models.ForeignKey(to='interactive.TestQuestion', null=True, related_name='alternatives'),
        ),
        migrations.AddField(
            model_name='testquestionalternative',
            name='target',
            field=models.ManyToManyField(verbose_name='tilsvarende resultat (lagre én gang for å få korrekte resultater)', to='interactive.TestResult', help_text='Velg resultatene dette alternativet svarer til.', blank=True),
        ),
        migrations.AddField(
            model_name='testquestionalternative',
            name='weights',
            field=models.TextField(validators=[interactive.models.user_test.validate_weight_syntax], verbose_name='vektlegging av resultater', help_text='Bestem hvor mye hvert resultat vektlegges ved valg av dette alternativet. Format er 3,1,4 (altså heltall) det 3 er vekten til det øveste resultatet osv. Hvis blank får alle vekt 1, og hvis listen ikke er lang nok får resten vekt 1', blank=True),
        ),
        migrations.AddField(
            model_name='testresult',
            name='test',
            field=models.ForeignKey(to='interactive.Test', null=True, related_name='results'),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='text',
            field=models.TextField(default='', verbose_name='spørsmål'),
        ),
        migrations.AlterField(
            model_name='testquestionalternative',
            name='text',
            field=models.TextField(verbose_name='svaralternativ'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='content',
            field=models.TextField(verbose_name='beskrivelse'),
        ),
    ]
