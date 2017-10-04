from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from image_cropping.fields import ImageRatioField


class BaseImageModel(models.Model):

    file = models.ImageField(
        max_length=100,
        verbose_name="Bildefil",
        upload_to="uploads/content"
    )

    def __str__(self):
        return "({}) {}".format(self.id, self.file.url if self.file else "")

    def image_thumb(self):
        if self.file:
            return '<img src="%s" style="max-width:100px;max-height:100px;"/>' % self.file.url
        else:
            return 'No image'

    image_thumb.allow_tags = True
    image_thumb.short_description = "Thumbnail"

    class Meta:
        abstract = True


class WithPicture(models.Model):
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

    class Meta:
        abstract = True

    def get_picture_url(self):
        return 'http://%s%s%s' % (Site.objects.get_current().domain, settings.MEDIA_URL, self.picture.name)


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
        self.view_counter += 1
        self.save(update_fields=["view_counter"])

    class Meta:
        abstract = True


class TimeStamped(models.Model):

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
        auto_now=True,
        null=True
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
        if not self.publication_date:
            return self.published
        if datetime.now() >= self.publication_date:
            return True
        return False

    def save(self, **kwargs):
        self.published = self.is_published
        return super().save(**kwargs)

    class Meta:
        abstract = True
