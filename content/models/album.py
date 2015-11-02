# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse

from .base import EditableMedia, BaseImageModel


class AlbumImage(BaseImageModel):
    """
    An album image.
    """

    description = models.TextField(
        verbose_name="Bildetekst",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Albumbilde"
        verbose_name_plural = "Albumbilder"


class Album(EditableMedia, models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Albumtittel",
        blank=False,
        null=True
    )
    images = models.ManyToManyField(
        AlbumImage,
        verbose_name="Bilder",
    )

    VISIBILITY_OPTIONS = (
        ('p', 'public'),
        ('u', 'users'),
        ('h', 'hidden')
    )

    visibility = models.CharField(
        max_length=1,
        verbose_name="Synlighet",
        choices=VISIBILITY_OPTIONS,
        default='h',
        blank=False
    )

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Album"

    def get_absolute_url(self):
        return reverse('album', kwargs={'pk': self.pk,'num': '0'})

    def is_visible(self, user=None):
        if self.visibility != 'p':
            if self.visibility != 'h' and user is not None:
                return user.is_authenticated()
            else:
                return False
        else:
            return True

    def __str__(self):
        return self.title
