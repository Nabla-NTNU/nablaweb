# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-06 23:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("nabladet", "0007_auto_20171017_0140"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="nablad",
            name="view_counter",
        ),
    ]
