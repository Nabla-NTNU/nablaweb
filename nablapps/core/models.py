"""
Abstract models to be included in other apps
"""
# Ignore pylint problems with Meta-classes
# pylint: disable=missing-docstring,too-few-public-methods
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models

from image_cropping.fields import ImageRatioField


class BaseImageModel(models.Model):
    """
    Abstract model for representing a single image.
    """

    file = models.ImageField(
        max_length=100, verbose_name="Bildefil", upload_to="uploads/content"
    )

    def __str__(self):
        return f"({self.id}) {self.file.url if self.file else ''}"

    def image_thumb(self):
        """Return a string containing html for showing a thumbnail of the image"""
        if not self.file:
            return "No image"
        return f'<img src="{self.file.url}" style="max-width:100px;max-height:100px;"/>'

    image_thumb.allow_tags = True
    image_thumb.short_description = "Thumbnail"

    class Meta:
        abstract = True


class WithPicture(models.Model):
    """
    Abstract model to be mixed in to models requiring a single image.
    """

    picture = models.ImageField(
        upload_to="uploads/news_pictures",
        null=True,
        blank=True,
        verbose_name="Bilde",
        help_text=(
            "Bilder som er større enn 770x300 px ser best ut. "
            "Du kan beskjære bildet etter opplasting."
        ),
    )

    cropping = ImageRatioField(
        "picture", "770x300", allow_fullsize=False, verbose_name="Beskjæring"
    )

    class Meta:
        abstract = True

    def get_picture_url(self):
        """Return the absolute url of the main picture"""
        domain = Site.objects.get_current().domain
        media_url = settings.MEDIA_URL
        filename = self.picture.name
        return f"http://{domain}{media_url}{filename}"


class TimeStamped(models.Model):
    """
    Abstract model which adds datetime fields indicating
    when the model was created and/or changed
    and fields indicating who did it.

    The user fields has to be updated manually or through
    the admin interface using ChangedByMixin.
    """

    created_date = models.DateTimeField(
        verbose_name="Publiseringsdato", auto_now_add=True, null=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Opprettet av",
        related_name="%(class)s_created",
        editable=False,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    last_changed_date = models.DateTimeField(
        verbose_name="Redigeringsdato", auto_now=True, null=True
    )

    last_changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Endret av",
        related_name="%(class)s_edited",
        editable=False,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    def has_been_edited(self):
        """Return whether the object has been changed since creation"""
        return abs((self.last_changed_date - self.created_date).seconds) > 1
