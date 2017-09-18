# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0010_auto_20150810_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='publication_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Publikasjonstid'),
        ),
        migrations.AddField(
            model_name='podcast',
            name='published',
            field=models.NullBooleanField(default=None, verbose_name='Publisert'),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='view_counter',
            field=models.IntegerField(default=0, editable=False, verbose_name='Visninger'),
        ),
    ]
