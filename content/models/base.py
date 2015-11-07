# -*- coding: utf-8 -*-


from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site

from image_cropping.fields import ImageRatioField
from .mixins import EditableMedia, PublicationManagerMixin, CommentsMixin


class BaseImageModel(models.Model):

    file = models.FileField(
        max_length=100,
        verbose_name="Bildefil",
        upload_to="uploads/content"
    )

    def get_absolute_url(self):
        return self.file.url

    def __str__(self):
        return "(" + str(self.id) + ") " + self.file.url

    class Meta:
        abstract = True


class Content(CommentsMixin, PublicationManagerMixin, EditableMedia, models.Model):

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

    @models.permalink
    def get_absolute_url(self):
        """
        Finner URL ved å reversere navnet på viewen.
        Krever at navnet på viewet er gitt ved modellnavn_detail
        """
        return (self.content_type.model + "_detail", (), {
            'pk': self.pk,
            'slug': self.slug
        })

    def get_picture_url(self):
        return 'http://%s%s%s' % (Site.objects.get_current().domain, settings.MEDIA_URL, self.picture.name)


class ContentImage(BaseImageModel):
    """
    An image associated with some content
    """

    class Meta:
        verbose_name = "Innholdsbilde"
        verbose_name_plural = "Innholdsbilder"
