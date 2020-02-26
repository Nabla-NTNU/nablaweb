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
            name="Choice",
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
                    "choice",
                    models.CharField(max_length=80, verbose_name="Navn på valg"),
                ),
                (
                    "votes",
                    models.IntegerField(default=0, verbose_name="Antall stemmer"),
                ),
                (
                    "creation_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="Lagt til"),
                ),
                (
                    "added_by",
                    models.CharField(max_length=100, verbose_name="Lagt til av"),
                ),
            ],
            options={"verbose_name": "valg", "verbose_name_plural": "valg",},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Poll",
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
                    "question",
                    models.CharField(max_length=1000, verbose_name="Spørsmål"),
                ),
                (
                    "creation_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="Opprettet"),
                ),
                ("publication_date", models.DateTimeField(verbose_name="Publisert")),
                (
                    "added_by",
                    models.CharField(max_length=100, verbose_name="Lagt til av"),
                ),
                (
                    "edit_date",
                    models.DateTimeField(auto_now=True, verbose_name="Sist endret"),
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
                        help_text="",
                        verbose_name="Brukere som har stemt",
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "avstemning",
                "verbose_name_plural": "avstemninger",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="choice",
            name="poll",
            field=models.ForeignKey(to="poll.Poll", on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
