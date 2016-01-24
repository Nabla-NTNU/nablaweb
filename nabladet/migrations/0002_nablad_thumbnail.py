# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nabladet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nablad',
            name='thumbnail',
            field=models.FileField(editable=False, upload_to='', null=True),
        ),
    ]
