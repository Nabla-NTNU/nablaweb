from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from content.models import (
    PublicationManagerMixin,
    TimeStamped,
    ViewCounterMixin,
    WithPicture,
)


class NewsBase(
    PublicationManagerMixin,
    TimeStamped,
    ViewCounterMixin,
    WithPicture,
):
    headline = models.CharField(
        verbose_name="tittel",
        max_length=100,
        blank=True)
    lead_paragraph = models.TextField(
        verbose_name="ingress",
        blank=True,
        help_text="Vises på forsiden og i artikkelen")
    body = models.TextField(
        verbose_name="brødtekst",
        blank=True,
        help_text=(
            "Vises kun i artikkelen. "
            "Man kan her bruke <a href=\"http://en.wikipedia.org/wiki/Markdown\" target=\"_blank\">"
            "markdown</a> for å formatere teksten."))
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.headline)
        return super().save(*args, **kwargs)


class News(NewsBase):

    content_type = models.ForeignKey(
        ContentType,
        editable=False,
        null=True
    )

    class Meta:
        verbose_name = "nyhet"
        verbose_name_plural = "nyheter"
        db_table = "content_news"

    def correct_picture(self):
        return self.picture

    def correct_cropping(self):
        return self.cropping

    @property
    def as_child_class(self):
        if hasattr(self, 'advert'):
            return self.advert
        elif hasattr(self, 'bedpres'):
            return self.bedpres
        else:
            return self

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        """
        Finner URL ved å reversere navnet på viewen.
        Krever at navnet på viewet er gitt ved modellnavn_detail
        """
        return reverse(self.content_type.model + "_detail", kwargs={
            'pk': self.pk,
            'slug': self.slug
        })
