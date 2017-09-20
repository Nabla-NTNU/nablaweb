from datetime import datetime
import logging

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from django_comments.models import Comment

logger = logging.getLogger(__name__)


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


class CommentsMixin(models.Model):
    allow_comments = models.BooleanField(
        blank=True,
        verbose_name="Tillat kommentarer",
        default=True,
        help_text="Hvorvidt kommentering er tillatt"
    )

    content_type = models.ForeignKey(
        ContentType,
        editable=False,
        null=True
    )

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """
        Override default method, so related comments are also deleted
        """
        comments = Comment.objects.filter(
            object_pk=self.pk,
            content_type=self.content_type
        )
        comments.delete()
        super(CommentsMixin, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(self.__class__)
        if not self.content_type or self.content_type != content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(CommentsMixin, self).save(*args, **kwargs)
