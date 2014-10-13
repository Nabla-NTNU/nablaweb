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
            field=models.DateTimeField(null=True, verbose_name=b'avmeldingsfrist', blank=True),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'P\xc3\xa5meldingsdato', null=True),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='number',
            field=models.PositiveIntegerField(help_text=b'K\xc3\xb8nummer som tilsvarer plass p\xc3\xa5 ventelisten/p\xc3\xa5meldingsrekkef\xc3\xb8lge.', null=True, verbose_name=b'k\xc3\xb8nummer', blank=True),
        ),
    ]
