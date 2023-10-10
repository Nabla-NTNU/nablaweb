# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventRegistration",
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
                    "date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Påmeldingsdato", null=True
                    ),
                ),
                (
                    "number",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Kønummer som tilsvarer plass på ventelisten/påmeldingsrekkefølge.",
                        verbose_name="kønummer",
                        null=True,
                    ),
                ),
                (
                    "attending",
                    models.BooleanField(
                        help_text="Hvis denne er satt til sann har man en plass på arrangementet ellers er det en ventelisteplass.",
                        verbose_name="har plass",
                        default=True,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="bruker",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "verbose_name": "påmelding",
                "verbose_name_plural": "påmeldte",
                "db_table": "content_eventregistration",
            },
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "news_ptr",
                    models.OneToOneField(
                        parent_link=True,
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                        to="news.News",
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "short_name",
                    models.CharField(
                        blank=True,
                        help_text="Brukes på steder hvor det ikke er plass til å skrive hele overskriften, for eksempel kalenderen.",
                        max_length=20,
                        null=True,
                        verbose_name="kort navn",
                    ),
                ),
                (
                    "organizer",
                    models.CharField(
                        blank=True,
                        help_text="Den som står bak arrangementet",
                        max_length=100,
                        verbose_name="organisert av",
                    ),
                ),
                ("location", models.CharField(max_length=100, verbose_name="sted")),
                ("event_start", models.DateTimeField(verbose_name="start", null=True)),
                (
                    "event_end",
                    models.DateTimeField(blank=True, verbose_name="slutt", null=True),
                ),
                (
                    "facebook_url",
                    models.CharField(
                        blank=True,
                        help_text="URL-en til det tilsvarende arrangementet på Facebook",
                        max_length=100,
                        verbose_name="facebook-url",
                    ),
                ),
                (
                    "registration_required",
                    models.BooleanField(verbose_name="påmelding", default=False),
                ),
                (
                    "registration_deadline",
                    models.DateTimeField(
                        blank=True, verbose_name="påmeldingsfrist", null=True
                    ),
                ),
                (
                    "registration_start",
                    models.DateTimeField(
                        blank=True, verbose_name="påmelding åpner", null=True
                    ),
                ),
                (
                    "deregistration_deadline",
                    models.DateTimeField(
                        blank=True, verbose_name="avmeldingsfrist", null=True
                    ),
                ),
                (
                    "places",
                    models.PositiveIntegerField(
                        blank=True, verbose_name="antall plasser", null=True
                    ),
                ),
                (
                    "has_queue",
                    models.NullBooleanField(
                        help_text="Om ventelisten er på, vil det være mulig å melde seg på selv om arrangementet er fullt. De som er i ventelisten vil automatisk bli påmeldt etter hvert som plasser blir ledige.",
                        verbose_name="har venteliste",
                    ),
                ),
                (
                    "open_for",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Hvilke grupper som får lov til å melde seg på arrangementet. Hvis ingen grupper er valgt er det åpent for alle.",
                        to="auth.Group",
                        verbose_name="Åpen for",
                    ),
                ),
            ],
            options={
                "permissions": (("administer", "Can administer models"),),
                "verbose_name": "arrangement",
                "verbose_name_plural": "arrangement",
                "db_table": "content_event",
            },
            # bases=('news.news', models.Model),
        ),
        migrations.AddField(
            model_name="eventregistration",
            name="event",
            field=models.ForeignKey(
                null=True, to="events.Event", on_delete=models.CASCADE
            ),
        ),
        migrations.AlterUniqueTogether(
            name="eventregistration",
            unique_together=set([("number", "attending"), ("event", "user")]),
        ),
    ]
