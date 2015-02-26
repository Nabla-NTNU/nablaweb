# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bedpres', '0002_auto_20140914_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bedpres',
            name='deregistration_deadline',
            field=models.DateTimeField(null=True, verbose_name='avmeldingsfrist', blank=True),
        ),
    ]
