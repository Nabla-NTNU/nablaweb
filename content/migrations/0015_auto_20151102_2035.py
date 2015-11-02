# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0014_auto_20151023_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='publication_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Publikasjonstid'),
        ),
    ]
