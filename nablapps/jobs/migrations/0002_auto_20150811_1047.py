# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advert',
            options={'ordering': ('-created_date', 'headline'), 'verbose_name': 'stillingsannonse', 'verbose_name_plural': 'stillingsannonser'},
        ),
        migrations.AlterField(
            model_name='advert',
            name='relevant_for_year',
            field=models.ManyToManyField(help_text='Hvilke årskull stillingsannonsen er relevant for.', to='nablapps.jobs.YearChoices', null=True, verbose_name='Årskull'),
        ),
    ]
