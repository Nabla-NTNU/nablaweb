"""
Abstract models to be included in other apps
"""
# Ignore pylint problems with Meta-classes
# pylint: disable=missing-docstring,too-few-public-methods
from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from image_cropping.fields import ImageRatioField


class BaseImageModel(models.Model):
    """
    Abstract model for representing a single image.
    """

    file = models.ImageField(
        max_length=100,
        verbose_name="Bildefil",
        upload_to="uploads/content"
    )

    def __str__(self):
        return f"({self.id}) {self.file.url if self.file else ''}"

    def image_thumb(self):
        """Return a string containing html for showing a thumbnail of the image"""
        if not self.file:
            return 'No image'
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
        help_text=("Bilder som er større enn 770x300 px ser best ut. "
                   "Du kan beskjære bildet etter opplasting."),
    )

    cropping = ImageRatioField(
        'picture',
        '770x300',
        allow_fullsize=False,
        verbose_name="Beskjæring"
    )

    class Meta:
        abstract = True

    def get_picture_url(self):
        """Return the absolute url of the main picture"""
        domain = Site.objects.get_current().domain
        media_url = settings.MEDIA_URL
        filename = self.picture.name
        return f'http://{domain}{media_url}{filename}'


class ViewCounterMixin(models.Model):
    """
    Adds view counting functionality. The corresponding view mixin needs to also be added.
    """
    view_counter = models.IntegerField(
        editable=False,
        default=0,
        verbose_name="Visninger"
    )

    def add_view(self):
        """Increase view count by one"""
        self.view_counter += 1
        self.save(update_fields=["view_counter"])

    class Meta:
        abstract = True


class TimeStamped(models.Model):
    """
    Abstract model which adds datetime fields indicating
    when the model was created and/or changed
    and fields indicating who did it.

    The user fields has to be updated manually or through
    the admin interface using ChangedByMixin.
    """

    created_date = models.DateTimeField(
        verbose_name="Publiseringsdato",
        auto_now_add=True,
        null=True
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
        verbose_name="Redigeringsdato",
        auto_now=True,
        null=True
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


class PublicationManagerMixin(models.Model):
    """
    Adds several options for managing publication.
    """

    publication_date = models.DateTimeField(
        editable=True,
        null=True,
        blank=True,
        verbose_name="Publikasjonstid"
    )

    published = models.NullBooleanField(
        default=True,
        verbose_name="Publisert",
        help_text="Dato har høyere prioritet enn dette feltet."
    )

    @property
    def is_published(self):
        """
        Return whether the object is considered published

        It is considered published if either
           - the publication date is not set and the published field is set to true
           - or the publication date is set and has passed.
        """
        return datetime.now() >= self.publication_date if self.publication_date else self.published

    def save(self, *args, **kwargs): # pylint: disable=W0221
        self.published = self.is_published
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
