"""
Models for nabladet app
"""
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.urls import reverse

from nablapps.core.models import TimeStamped, WithPicture
from nablapps.news.models import TextContent

from .pdfthumbnailer import thumbnail_pdf


class Nablad(TimeStamped, WithPicture, TextContent):
    """Model representing a nablad"""

    pub_date = models.DateField(
        verbose_name="publisert", blank=False, null=True, help_text="Publikasjonsdato"
    )

    file = models.FileField(
        upload_to="nabladet",
        verbose_name="PDF-fil",
        help_text="Filnavn. OBS: opplasting kan ta rundt ett minutt, så bare trykk 'Lagre' én gang.",
        storage=FileSystemStorage(location=settings.PROTECTED_MEDIA_ROOT),
    )

    file_nsfw = models.FileField(
        upload_to="nabladet",
        verbose_name="PDF-fil NSFW",
        help_text="Filnavn",
        blank=True,
        null=True,
        storage=FileSystemStorage(location=settings.PROTECTED_MEDIA_ROOT),
    )

    thumbnail = models.FileField(
        editable=False,
        null=True,
        storage=FileSystemStorage(location=settings.PROTECTED_MEDIA_ROOT),
    )

    is_public = models.BooleanField(
        default=False,
        help_text="Bestemmer om brukere som ikke er logget inn kan se dette Nabladet.",
        verbose_name="Offentlig tilgjengelig",
    )

    filename = models.TextField(blank=True, editable=False)

    class Meta:
        verbose_name = "nablad"
        verbose_name_plural = "nablad"
        ordering = ("-pub_date",)

    def update_thumbnail(self):
        """Create a thumbnail of the first page of the pdf of the nablad."""
        absolute_pdfpath = os.path.join(settings.PROTECTED_MEDIA_ROOT, self.file.name)
        absolute_thumbpath = thumbnail_pdf(absolute_pdfpath)
        self.thumbnail.name = os.path.relpath(
            absolute_thumbpath, start=settings.PROTECTED_MEDIA_ROOT
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file:
            if self.filename != self.file.name:
                self.filename = self.file.name
                self.update_thumbnail()
        if not self.thumbnail and self.file:
            self.update_thumbnail()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        """Get canonical url for nablad"""
        return reverse("nablad_detail", kwargs={"pk": self.pk, "slug": self.slug})

    def get_model_name(self):
        return self._meta.verbose_name
