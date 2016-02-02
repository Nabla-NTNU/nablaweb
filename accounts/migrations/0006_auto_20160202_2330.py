# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_likepress'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='nablauser',
            managers=[
                ('objects', accounts.models.NablaUserManager()),
            ],
        ),
    ]
