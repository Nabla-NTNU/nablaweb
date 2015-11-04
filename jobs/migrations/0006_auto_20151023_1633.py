# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_auto_20151003_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='publication_date',
            field=models.DateTimeField(null=True, verbose_name='Publikasjonstid'),
        ),
        migrations.AddField(
            model_name='company',
            name='published',
            field=models.NullBooleanField(verbose_name='Publisert', default=None),
        ),
    ]
