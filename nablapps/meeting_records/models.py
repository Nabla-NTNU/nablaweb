"""
Models for meeting_records app
"""

from datetime import date

from django.db import models
from django.urls import reverse

from nablapps.core.models import TimeStamped


class MeetingRecord(TimeStamped):
    """
    Model for a meeting record.

    Assumes the meeting record is in the format of a pdf-file.
    """

    title = models.CharField(verbose_name="tittel", max_length=100, blank=False)

    slug = models.SlugField(
        null=True,
        blank=True,
        help_text="Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres",
    )

    description = models.TextField(verbose_name="Beskrivelse", blank=True)

    pub_date = models.DateField(
        verbose_name="publisert",
        blank=False,
        null=True,
        default=date.today,
        help_text="Publikasjonsdato",
    )

    file = models.FileField(
        upload_to="meeting_records",
        verbose_name="PDF-fil",
        null=True,
        blank=False,
        help_text="Filnavn",
    )

    class Meta:
        verbose_name = "Møtereferat"
        verbose_name_plural = "Møtereferater"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Return the canonical url for the record"""
        return reverse(
            "meetingrecord_detail", kwargs={"pk": self.pk, "slug": self.slug}
        )
