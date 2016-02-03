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

    album = models.ForeignKey(
        'content.Album',
        verbose_name="Album",
        related_name="images",
        null=True
    )

    num = models.PositiveIntegerField(
        verbose_name="Nummer",
        null=True
    )

    def get_absolute_url(self):
        return reverse('album_image', kwargs={
            "pk": self.album.id,
            "num": self.num+1
        })

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
        return reverse('album', kwargs={'pk': self.pk})

    def is_visible(self, user=None):
        if self.visibility != 'p':
            if self.visibility != 'h' and user is not None:
                return user.is_authenticated()
            else:
                return False
        else:
            return True

    @property
    def first(self):
        try:
            return self.images.get(num=0)
        except AlbumImage.DoesNotExist:
            return None

    def __str__(self):
        return self.title
