# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interactive', '0005_adventdoor_is_lottery'),
    ]

    operations = [
        migrations.AddField(
            model_name='adventdoor',
            name='participating_users',
            field=models.ManyToManyField(related_name='participating_in_doors', blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
