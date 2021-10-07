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
            name="Exchange",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                        auto_created=True,
                    ),
                ),
                (
                    "retning",
                    models.CharField(
                        max_length=6,
                        help_text="Retning",
                        choices=[
                            ("biofys", "Biofysikk og medisinteknologi"),
                            ("indmat", "Industriell matematikk"),
                            ("tekfys", "Teknisk fysikk"),
                        ],
                    ),
                ),
                ("start", models.DateField(help_text="Dato utveksling startet")),
                ("end", models.DateField(help_text="Dato utveksling sluttet")),
                (
                    "student",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
                    ),
                ),
            ],
            options={
                "ordering": ["student"],
                "verbose_name_plural": "utvekslinger",
                "verbose_name": ("utveksling",),
            },
        ),
        migrations.CreateModel(
            name="Info",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                        auto_created=True,
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default="",
                        max_length=50,
                        help_text="Tittelen til innholdet",
                        verbose_name="tittel",
                    ),
                ),
                (
                    "body",
                    models.TextField(
                        blank=True,
                        help_text='Man kan her bruke <a href="http://en.wikipedia.org/wiki/Markdown" target="_blank">markdown</a> for å formatere teksten.',
                        verbose_name="brødtekst",
                    ),
                ),
                (
                    "ex",
                    models.ForeignKey(to="exchange.Exchange", on_delete=models.CASCADE),
                ),
            ],
            options={
                "verbose_name_plural": "info",
                "verbose_name": ("info",),
            },
        ),
        migrations.CreateModel(
            name="University",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                        auto_created=True,
                    ),
                ),
                (
                    "univ_navn",
                    models.CharField(
                        default="",
                        max_length=50,
                        help_text="Navnet til universitetet",
                        verbose_name="universitets navn",
                    ),
                ),
                (
                    "desc",
                    models.TextField(
                        blank=True,
                        help_text="En kort beskrivelse av universitetet. Valgfritt.",
                        verbose_name="beskrivelse",
                    ),
                ),
                (
                    "land",
                    models.CharField(
                        default="",
                        max_length=30,
                        help_text="Landet universitetet ligger i",
                        verbose_name="land",
                    ),
                ),
            ],
            options={
                "ordering": ["univ_navn"],
                "verbose_name_plural": "universiteter",
                "verbose_name": "universitet",
            },
        ),
        migrations.AddField(
            model_name="exchange",
            name="univ",
            field=models.ForeignKey(to="exchange.University", on_delete=models.CASCADE),
        ),
    ]
