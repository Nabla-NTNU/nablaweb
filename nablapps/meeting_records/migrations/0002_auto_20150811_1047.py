# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_records', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingrecord',
            name='file',
            field=models.FileField(help_text='Filnavn', upload_to='meeting_records', null=True, verbose_name='PDF-fil'),
        ),
    ]
