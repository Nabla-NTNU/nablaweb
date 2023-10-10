# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [
        ("meeting_records", "0001_initial"),
        ("meeting_records", "0002_auto_20150811_1047"),
        ("meeting_records", "0003_remove_subclassing_news"),
    ]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MeetingRecord",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        serialize=False,
                        auto_created=True,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        null=True, verbose_name="Publiseringsdato", auto_now_add=True
                    ),
                ),
                (
                    "last_changed_date",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Redigeringsdato"
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="tittel")),
                (
                    "description",
                    models.TextField(verbose_name="Beskrivelse", blank=True),
                ),
                (
                    "pub_date",
                    models.DateField(
                        help_text="Publikasjonsdato",
                        default=datetime.date.today,
                        null=True,
                        verbose_name="publisert",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        help_text="Filnavn",
                        upload_to="meeting_records",
                        null=True,
                        verbose_name="PDF-fil",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="meetingrecord_created",
                        verbose_name="Opprettet av",
                        to=settings.AUTH_USER_MODEL,
                        editable=False,
                        null=True,
                        blank=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "last_changed_by",
                    models.ForeignKey(
                        related_name="meetingrecord_edited",
                        verbose_name="Endret av",
                        to=settings.AUTH_USER_MODEL,
                        editable=False,
                        null=True,
                        blank=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres",
                        null=True,
                        blank=True,
                    ),
                ),
            ],
            options={
                "ordering": ("-pub_date",),
                "verbose_name_plural": "Møtereferater",
                "verbose_name": "Møtereferat",
            },
        ),
    ]
