from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser

from content.models.base import TimeStamped, ViewCounterMixin, BaseImageModel


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
        return reverse('album_image', kwargs={
            "pk": self.album.id,
            "num": self.num+1
        })

    class Meta:
        verbose_name = "Albumbilde"
        verbose_name_plural = "Albumbilder"
        db_table = "content_albumimage"


class Album(TimeStamped, ViewCounterMixin, models.Model):
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
        return reverse('album', kwargs={'pk': self.pk})

    def is_visible(self, user=AnonymousUser()):
        return self.visibility == 'p' or (self.visibility == 'u' and user.is_authenticated())

    @property
    def first(self):
        try:
            return self.images.get(num=0)
        except AlbumImage.DoesNotExist:
            return None

    def __str__(self):
        return self.title
