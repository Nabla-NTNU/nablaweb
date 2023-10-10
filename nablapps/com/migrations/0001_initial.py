# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ComMembership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "story",
                    models.TextField(
                        help_text="Ansvarsområde eller lignende",
                        verbose_name="Beskrivelse",
                        blank=True,
                    ),
                ),
                (
                    "joined_date",
                    models.DateField(
                        help_text="Dato personen ble med i komiteen",
                        null=True,
                        verbose_name="Ble med",
                        blank=True,
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Aktiv?")),
                (
                    "com",
                    models.ForeignKey(
                        verbose_name="Komité", to="auth.Group", on_delete=models.CASCADE
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
                    ),
                ),
            ],
            options={
                "verbose_name": "komitemedlem",
                "verbose_name_plural": "komitemedlemmer",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ComPage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Teksten på komitésiden",
                        verbose_name="Beskrivelse",
                        blank=True,
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        verbose_name="Slug til URL-er",
                        unique=True,
                        max_length=50,
                        editable=False,
                    ),
                ),
                (
                    "last_changed_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Sist redigert", null=True
                    ),
                ),
                ("com", models.ForeignKey(to="auth.Group", on_delete=models.CASCADE)),
                (
                    "last_changed_by",
                    models.ForeignKey(
                        related_name="compage_edited",
                        blank=True,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        verbose_name="Sist endret av",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "verbose_name": "komiteside",
                "verbose_name_plural": "komitesider",
            },
            bases=(models.Model,),
        ),
    ]
