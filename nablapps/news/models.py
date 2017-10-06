from django.utils import timezone
from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse


from content.models import (
    PublicationManagerMixin,
    TimeStamped,
    ViewCounterMixin,
    WithPicture,
)

from django.conf import settings


class TimeStampedWhileRefactoring(models.Model):

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
        null=True
    )

    last_changed_date = models.DateTimeField(
        verbose_name="Redigeringsdato",
        default=timezone.now,
        null=True,
        blank=True,
    )

    last_changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Endret av",
        related_name="%(class)s_edited",
        editable=False,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

    def has_been_edited(self):
        return abs((self.last_changed_date - self.created_date).seconds) > 1

    def save(self, *args, **kwargs):
        #self.last_changed_date = timezone.now()
        super().save(*args, **kwargs)


class TextContent(models.Model):
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


class NewsBase(
    PublicationManagerMixin,
    TimeStampedWhileRefactoring,
    ViewCounterMixin,
    WithPicture,
    TextContent
):

    def correct_picture(self):
        return self.picture

    def correct_cropping(self):
        return self.cropping

    class Meta:
        abstract = True


    def __str__(self):
        return self.headline


class NewsArticle(NewsBase):
    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"pk": self.pk, "slug": self.slug})


class News(NewsBase):

    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType,
        editable=False,
        null=True
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "nyhet"
        verbose_name_plural = "nyheter"
        db_table = "content_news"

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()
