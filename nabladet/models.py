# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.db import models
from content.models import News
from content.utils import thumbnail_pdf


class Nablad(News):
    pub_date = models.DateField(
        verbose_name='publisert',
        blank=False,
        null=True,
        help_text="Publikasjonsdato"
    )

    file = models.FileField(
        upload_to='nabladet',
        verbose_name='PDF-fil',
        help_text="Filnavn"
    )

    thumbnail = models.FileField(
        editable=False,
        null=True
    )

    is_public = models.BooleanField(
        default=False,
        help_text="Bestemmer om brukere som ikke er logget inn kan se dette Nabladet.",
        verbose_name="Offentlig tilgjengelig"
    )

    class Meta:
        verbose_name = 'nablad'
        verbose_name_plural = 'nablad'
        ordering = ("-pub_date",)

    def update_thumbnail(self):
        self.thumbnail.name = os.path.relpath(thumbnail_pdf(os.path.join(settings.MEDIA_ROOT, self.file.name)),
                                              start=settings.MEDIA_ROOT)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.thumbnail and self.file:
            self.update_thumbnail()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.headline
