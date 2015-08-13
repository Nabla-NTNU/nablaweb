# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0009_auto_20150808_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='extra_markdown',
            field=models.TextField(help_text='Ekstra markdown for å putte inn videoer etc.', verbose_name='Ekstra markdown', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='podcast',
            name='file',
            field=models.FileField(verbose_name='lydfil', blank=True, help_text='Filformat: MP3', upload_to='podcast'),
            preserve_default=True,
        ),
    ]
