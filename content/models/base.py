# -*- coding: utf-8 -*-


from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from django_comments.models import Comment
from image_cropping.fields import ImageRatioField
from .mixins import EditableMedia, PublicationManagerMixin


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


class Content(PublicationManagerMixin, EditableMedia, models.Model):
    # Bildeopplasting med resizing og cropping
    picture = models.ImageField(
        upload_to="news_pictures",
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

    # Slugs
    slug = models.SlugField(
        null=True,
        blank=True,
        help_text="Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres"
    )

    allow_comments = models.BooleanField(
        blank=True,
        verbose_name="Tillat kommentarer",
        default=True,
        help_text="Hvorvidt kommentering er tillatt"
    )

    # content_type is here so that we can know which subclass of Content/News this is. (Polymorphism)
    content_type = models.ForeignKey(ContentType, editable=False, null=True)

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

    def has_been_edited(self):
        return abs((self.last_changed_date - self.created_date).seconds) > 1

    def get_picture_url(self):
        return 'http://%s%s%s' % (Site.objects.get_current().domain, settings.MEDIA_URL, self.picture.name)

    def delete(self, *args, **kwargs):
        """
        Override default method, so related comments are also deleted
        """
        comments = Comment.objects.filter(object_pk=self.pk,
                                          content_type=self.content_type)
        comments.delete()
        super(Content, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(Content, self).save(*args, **kwargs)


class ContentImage(BaseImageModel):
    """
    An image associated with some content
    """

    class Meta:
        verbose_name = "Innholdsbilde"
        verbose_name_plural = "Innholdsbilder"
