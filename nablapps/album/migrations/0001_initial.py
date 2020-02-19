# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Album",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Publiseringsdato", null=True
                    ),
                ),
                (
                    "last_changed_date",
                    models.DateTimeField(
                        verbose_name="Redigeringsdato", null=True, auto_now=True
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=100, null=True, verbose_name="Albumtittel"
                    ),
                ),
                (
                    "visibility",
                    models.CharField(
                        choices=[("p", "public"), ("u", "users"), ("h", "hidden")],
                        max_length=1,
                        verbose_name="Synlighet",
                        default="h",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="album_created",
                        editable=False,
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Opprettet av",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "last_changed_by",
                    models.ForeignKey(
                        related_name="album_edited",
                        editable=False,
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Endret av",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "view_counter",
                    models.IntegerField(
                        editable=False, verbose_name="Visninger", default=0
                    ),
                ),
            ],
            options={
                "verbose_name": "Album",
                "verbose_name_plural": "Album",
                "db_table": "content_album",
            },
        ),
        migrations.CreateModel(
            name="AlbumImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                    ),
                ),
                (
                    "file",
                    models.ImageField(
                        verbose_name="Bildefil", upload_to="uploads/content"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Bildetekst", null=True),
                ),
                (
                    "album",
                    models.ForeignKey(
                        related_name="images",
                        to="album.Album",
                        verbose_name="Album",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                ("num", models.PositiveIntegerField(verbose_name="Nummer", null=True)),
            ],
            options={
                "verbose_name": "Albumbilde",
                "verbose_name_plural": "Albumbilder",
                "db_table": "content_albumimage",
            },
        ),
    ]
