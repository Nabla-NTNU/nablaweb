# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='deregistration_deadline',
            field=models.DateTimeField(null=True, verbose_name='avmeldingsfrist', blank=True),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Påmeldingsdato', null=True),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='number',
            field=models.PositiveIntegerField(help_text='Kønummer som tilsvarer plass på ventelisten/påmeldingsrekkefølge.', null=True, verbose_name='kønummer', blank=True),
        ),
    ]
