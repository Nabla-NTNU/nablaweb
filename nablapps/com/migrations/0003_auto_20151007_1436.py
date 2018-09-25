# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('com', '0002_committee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='committee',
            name='leader',
            field=models.ForeignKey(blank=True, verbose_name='Leder', to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
    ]
