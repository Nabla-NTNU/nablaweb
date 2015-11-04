# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_company_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='images',
        ),
    ]
