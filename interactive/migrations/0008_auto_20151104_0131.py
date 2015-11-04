# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0007_adventdoor_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizreply',
            name='start',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='duration',
            field=models.PositiveIntegerField(null=True, help_text='Tid til å fullføre quizen målt i sekunder.', blank=True, verbose_name='Tidsbegrensning'),
        ),
    ]
