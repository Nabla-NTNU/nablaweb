# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [
        ("poll", "0001_initial"),
        ("poll", "0002_auto_20150401_1806"),
        ("poll", "0003_auto_20150925_2315"),
        ("poll", "0004_poll_is_user_poll"),
        ("poll", "0005_auto_20150926_0938"),
        ("poll", "0006_auto_20150926_1409"),
        ("poll", "0007_poll_content_type"),
        ("poll", "0008_remove_poll_content_type"),
    ]

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Poll",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        verbose_name="ID",
                        serialize=False,
                    ),
                ),
                (
                    "question",
                    models.CharField(max_length=1000, verbose_name="Spørsmål"),
                ),
                (
                    "creation_date",
                    models.DateTimeField(verbose_name="Opprettet", auto_now_add=True),
                ),
                ("publication_date", models.DateTimeField(verbose_name="Publisert")),
                (
                    "edit_date",
                    models.DateTimeField(verbose_name="Sist endret", auto_now=True),
                ),
                (
                    "is_current",
                    models.BooleanField(
                        default=True, verbose_name="Nåværende avstemning?"
                    ),
                ),
                (
                    "users_voted",
                    models.ManyToManyField(
                        to=settings.AUTH_USER_MODEL,
                        editable=False,
                        verbose_name="Brukere som har stemt",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL,
                        editable=False,
                        verbose_name="Lagt til av",
                        related_name="poll_created_by",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "is_user_poll",
                    models.BooleanField(
                        default=False, editable=False, verbose_name="Er brukerpoll"
                    ),
                ),
            ],
            options={
                "verbose_name": "Avstemning",
                "verbose_name_plural": "Avstemninger",
            },
        ),
        migrations.CreateModel(
            name="Choice",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        verbose_name="ID",
                        serialize=False,
                    ),
                ),
                (
                    "choice",
                    models.CharField(max_length=80, verbose_name="Navn på valg"),
                ),
                (
                    "votes",
                    models.IntegerField(default=0, verbose_name="Antall stemmer"),
                ),
                (
                    "creation_date",
                    models.DateTimeField(verbose_name="Lagt til", auto_now_add=True),
                ),
                (
                    "poll",
                    models.ForeignKey(
                        to="poll.Poll", related_name="choices", on_delete=models.CASCADE
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL,
                        editable=False,
                        verbose_name="Lagt til av",
                        help_text="Hvem som la til valget i avstemningen",
                        related_name="choice_created_by",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "verbose_name": "valg",
                "verbose_name_plural": "valg",
            },
        ),
    ]
