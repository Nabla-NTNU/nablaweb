# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('jobs', '0001_initial'),
        ('bedpres', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bedpres',
            name='company',
            field=models.ForeignKey(verbose_name='Bedrift', to='jobs.Company', help_text='Hvilken bedrift som står bak bedriftspresentasjonen'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bedpres',
            name='open_for',
            field=models.ManyToManyField(help_text='Hvilke grupper som får lov til å melde seg på arrangementet. Hvis ingen grupper er valgt er det åpent for alle.', to='auth.Group', null=True, verbose_name='åpen for', blank=True),
            preserve_default=True,
        ),
    ]
