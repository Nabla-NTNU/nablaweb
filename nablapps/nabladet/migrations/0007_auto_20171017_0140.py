# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 01:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("nabladet", "0006_news_ptr_to_id_20171006_1559"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="nablad",
            name="publication_date",
        ),
        migrations.RemoveField(
            model_name="nablad",
            name="published",
        ),
    ]
