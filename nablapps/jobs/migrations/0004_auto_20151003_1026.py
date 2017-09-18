# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0003_auto_20150904_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='edit_listeners',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='view_counter',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
