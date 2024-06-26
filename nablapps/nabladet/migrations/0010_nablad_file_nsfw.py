# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-04 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nabladet", "0009_nablad_filename"),
    ]

    operations = [
        migrations.AddField(
            model_name="nablad",
            name="file_nsfw",
            field=models.FileField(
                blank=True,
                help_text="Filnavn",
                null=True,
                upload_to="nabladet",
                verbose_name="PDF-fil NSFW",
            ),
        ),
    ]
