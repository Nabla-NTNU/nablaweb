from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site

from image_cropping.fields import ImageRatioField
from .mixins import PublicationManagerMixin, TimeStamped, ViewCounterMixin


class BaseImageModel(models.Model):

    file = models.ImageField(
        max_length=100,
        verbose_name="Bildefil",
        upload_to="uploads/content"
    )

    def __str__(self):
        return "(" + str(self.id) + ") " + self.file.url

    def image_thumb(self):
        if self.file:
            return '<img src="%s" style="max-width:100px;max-height:100px;"/>' % self.file.url
        else:
            return 'No image'

    image_thumb.allow_tags = True
    image_thumb.short_description = "Thumbnail"

    class Meta:
        abstract = True


class ContentBase(models.Model):

    picture = models.ImageField(
        upload_to="uploads/news_pictures",
        null=True,
        blank=True,
        verbose_name="Bilde",
        help_text="Bilder som er større enn 770x300 px ser best ut. Du kan beskjære bildet etter opplasting."
    )

    cropping = ImageRatioField(
        'picture',
        '770x300',
        allow_fullsize=False,
        verbose_name="Beskjæring"
    )

    slug = models.SlugField(
        null=True,
        blank=True,
        help_text="Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres"
    )

    class Meta:
        abstract = True

    def get_picture_url(self):
        return 'http://%s%s%s' % (Site.objects.get_current().domain, settings.MEDIA_URL, self.picture.name)


class Content(PublicationManagerMixin, TimeStamped, ViewCounterMixin, ContentBase):
    class Meta:
        abstract = True
