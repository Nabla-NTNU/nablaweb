# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0009_auto_20150914_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='edit_listeners',
            field=models.ManyToManyField(default=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='album',
            name='published',
            field=models.BooleanField(verbose_name='Publisert', default=False),
        ),
        migrations.AddField(
            model_name='album',
            name='view_counter',
            field=models.IntegerField(editable=False, default=0),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='edit_listeners',
            field=models.ManyToManyField(default=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='published',
            field=models.BooleanField(verbose_name='Publisert', default=False),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='view_counter',
            field=models.IntegerField(editable=False, default=0),
        ),
        migrations.AddField(
            model_name='news',
            name='edit_listeners',
            field=models.ManyToManyField(default=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='news',
            name='published',
            field=models.BooleanField(verbose_name='Publisert', default=False),
        ),
        migrations.AddField(
            model_name='news',
            name='view_counter',
            field=models.IntegerField(editable=False, default=0),
        ),
    ]
