# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20150811_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='relevant_for_year',
            field=models.ManyToManyField(verbose_name='Årskull', help_text='Hvilke årskull stillingsannonsen er relevant for.', to='jobs.YearChoices'),
        ),
    ]
