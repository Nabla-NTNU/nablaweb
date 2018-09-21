"""
Models for album app
"""
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser

from content.models import TimeStamped, ViewCounterMixin, BaseImageModel


class AlbumImage(BaseImageModel):
    """
    An album image.

    Each album image is associated with a single album
    """

    description = models.TextField(
        verbose_name="Bildetekst",
        blank=True,
        null=True
    )

    album = models.ForeignKey(
        'album.Album',
        verbose_name="Album",
        related_name="images",
        null=True
    )

    num = models.PositiveIntegerField(
        verbose_name="Nummer",
        null=True
    )

    def get_absolute_url(self):
        """Get canonical url for image"""
        return reverse('album_image',
                       kwargs={"pk": self.album.id, "num": self.num+1})

    class Meta:
        verbose_name = "Albumbilde"
        verbose_name_plural = "Albumbilder"
        db_table = "content_albumimage"


class Album(TimeStamped, ViewCounterMixin, models.Model):
    """
    Model representing an album which is a collection of images.
    """
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
        db_table = "content_album"

    def get_absolute_url(self):
        """Return canonical url for album"""
        return reverse('album', kwargs={'pk': self.pk})

    def is_visible(self, user=AnonymousUser()):
        """
        Return whether this album is visible for the supplied user.

        If visibility is 'p' then all users can see the album.
        If visibility is 'u' all logged in users can see the album.
        All logged in users with the permission to change albums can see the album.
        """
        return (self.visibility == 'p'
                or self.visibility == 'u' and user.is_authenticated()
                or user.has_perm('content.change_album'))

    @property
    def first(self):
        """Get the image which is considered to be the first in the album"""
        return self.images.order_by('num').first()

    def __str__(self):
        return self.title
