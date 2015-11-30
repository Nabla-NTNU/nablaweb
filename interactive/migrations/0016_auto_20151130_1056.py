# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0015_adventdoor_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='publication_date',
            field=models.DateTimeField(null=True, verbose_name='Publikasjonstid', blank=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='published',
            field=models.NullBooleanField(default=True, verbose_name='Publisert', help_text='Dato har høyere prioritet enn dette feltet.'),
        ),
    ]
