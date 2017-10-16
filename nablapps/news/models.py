from django.utils import timezone
from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from image_cropping.fields import ImageRatioField

from content.models import (
    PublicationManagerMixin,
    TimeStamped,
    ViewCounterMixin,
    WithPicture,
)


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


class NewsArticle(
    PublicationManagerMixin,
    TimeStamped,
    ViewCounterMixin,
    WithPicture,
    TextContent
):

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"pk": self.pk, "slug": self.slug})


class News(models.Model):

    # Fields for referencing objects of different contenttype
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Fields for sorting and prioritizing on the frontpage
    created_date = models.DateTimeField(
        auto_now_add=True,
        null=True
    )
    bump_time = models.DateTimeField(
        default=timezone.now,
        blank=False,
    )
    visible = models.BooleanField(default=True)
    sticky = models.BooleanField(default=False)

    # Fields to override the content from the content_object
    title_override = models.CharField(
        verbose_name="tittel",
        max_length=100,
        blank=True)
    text_override = models.TextField(
        verbose_name="ingress",
        blank=True,
        help_text="Vises på forsiden og i artikkelen")
    picture_override = models.ImageField(
        upload_to="uploads/news_pictures",
        null=True,
        blank=True,
        verbose_name="Bilde",
        help_text="Bilder som er større enn 770x300 px ser best ut. Du kan beskjære bildet etter opplasting.")
    cropping_override = ImageRatioField(
        'picture',
        '770x300',
        allow_fullsize=False,
        verbose_name="Beskjæring")

    class Meta:
        verbose_name = "nyhet"
        verbose_name_plural = "nyheter"
        db_table = "content_news"
        ordering = ("-sticky", "-bump_time",)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

    @property
    def headline(self):
        return self.title_override or self.content_object.headline

    @property
    def lead_paragraph(self):
        return self.text_override or self.content_object.lead_paragraph

    @property
    def picture(self):
        return self.picture_override or self.content_object.picture

    @property
    def cropping(self):
        return self.cropping_override or self.content_object.cropping
