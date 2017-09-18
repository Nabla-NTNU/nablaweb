# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poll', '0002_auto_20150401_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='added_by',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='added_by',
        ),
        migrations.AddField(
            model_name='choice',
            name='created_by',
            field=models.ForeignKey(editable=False, verbose_name='Lagt til av', null=True, related_name='choice_created_by', help_text='Hvem som la til valget i avstemningen', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='poll',
            name='created_by',
            field=models.ForeignKey(editable=False, verbose_name='Lagt til av', null=True, related_name='poll_created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
