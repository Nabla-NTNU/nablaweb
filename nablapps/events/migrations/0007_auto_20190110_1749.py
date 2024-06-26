# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-10 17:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0006_remove_event_view_counter"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="eventregistration",
            unique_together=set([("event", "user")]),
        ),
        migrations.AlterModelOptions(
            name="eventregistration",
            options={
                "ordering": ("id",),
                "verbose_name": "påmelding",
                "verbose_name_plural": "påmeldte",
            },
        ),
        migrations.RemoveField(
            model_name="eventregistration",
            name="number",
        ),
    ]
