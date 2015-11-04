# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_remove_company_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='published',
            field=models.NullBooleanField(help_text='Dato har høyere prioritet enn dette feltet.', verbose_name='Publisert', default=True),
        ),
    ]
