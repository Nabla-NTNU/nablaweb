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
    WithPicture,
)


class TextContent(models.Model):
    """
    Some common fields for things that are possible to add to the front page.
    """
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
    WithPicture,
    TextContent
):
    """
    Simple article model

    Used mostly for small news announcements.
    Is possible to add to the front page.
    """
    class Meta:
        verbose_name = "Nyhetsartikkel"
        verbose_name_plural = "Nyhetsartikler"

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"pk": self.pk, "slug": self.slug})


class FrontPageNews(models.Model):
    """
    Things that turn up on the frontpage

    Each frontpage entity links to different types of content using a generic relation.

    It is assumed that the related object implements the fields:
    headline, lead_paragraph, picture and cropping, just as NewsArticle.
    This is not ideal, and it might change in the future, or it might not.
    """

    # Fields for referencing objects of different contenttype
    # See https://docs.djangoproject.com/en/1.11/ref/contrib/contenttypes/#generic-relations
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Fields for sorting and prioritizing on the frontpage
    created_date = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name="Dato laget",
        help_text="Dette feltet gjør egentlig ingenting. Brukes kun for å se når nyheten ble laget."
    )
    bump_time = models.DateTimeField(
        default=timezone.now,
        blank=False,
        verbose_name="Sorteringstid",
        help_text=("Tiden nyheten ble bumpet opp til toppen av forsiden. "
                   "Brukes som felt for å sortere nyhetene.")
    )
    visible = models.BooleanField(
        default=True, verbose_name="Er synlig",
        help_text="Sett dette feltet til usann for å skjule nyheten fra forsiden")
    sticky = models.BooleanField(
        default=False, verbose_name="Klebrig",
        help_text="Blir værende på toppen. Dvs. sorters foran alle andre nyheter.")

    # Fields to override the content from the content_object
    title_override = models.CharField(
        verbose_name="tittel",
        max_length=100,
        blank=True)
    text_override = models.TextField(
        verbose_name="tekst",
        blank=True)
    picture_override = models.ImageField(
        upload_to="uploads/frontpageoverride",
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
        verbose_name = "Forsidenyhet"
        verbose_name_plural = "Forsidenyheter"
        ordering = ("-sticky", "-bump_time",)

    def __str__(self):
        return self.headline

    @property
    def obj(self):
        """
        In case the content_object does not exist, return a dummy object to not crash the site.
        """
        return self.content_object or DummyContentObject()

    def get_absolute_url(self):
        return self.obj.get_absolute_url()

    @property
    def headline(self):
        return self.title_override or self.obj.headline

    @property
    def lead_paragraph(self):
        return self.text_override or self.obj.lead_paragraph

    @property
    def picture(self):
        return self.picture_override or self.obj.picture

    @property
    def cropping(self):
        return self.cropping_override or self.obj.cropping

    def bump(self):
        self.bump_time = timezone.now()
        self.save(update_fields=["bump_time"])


class DummyContentObject(object):
    """
    Class used to make dummy objects
    """
    headline = "Invalid object"
    lead_paragraph = "This object does not exist. Someone has f**ked up."
    picture = None
    cropping = None

    @staticmethod
    def get_absolute_url():
        return "/"
