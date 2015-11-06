from django.db import models
from django_nyt.utils import notify
from django.conf import settings
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django_comments.models import Comment


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
        self.save()

    class Meta:
        abstract = True


class EditMessageMixin(models.Model):
    """
    Sends notifications if the object is changed.
    """

    edit_listeners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        verbose_name="Lyttere",
        help_text="Brukere som overvåker dette objektet"
    )

    message_key = None
    notification_url = None
    watch_fields = []
    old_field_format = "__old_{field}"

    def __init__(self, *args, **kwargs):
        super(EditMessageMixin, self).__init__(*args, **kwargs)
        if self.id:
            for field in self.watch_fields:
                old = getattr(self, field)
                setattr(self,
                        self.old_field_format.format(field=field), old)

    def get_message_key(self):
        if self.message_key:
            return self.message_key
        else:
            return "{app_label}_{model_name}_{id}".format(
                app_label=self._meta.app_label,
                model_name=self._meta.model_name,
                id=self.id
            )

    def get_notification_url(self):
        if self.notification_url:
            return self.notification_url
        else:
            return self.get_absolute_url()

    def notify(self, message):
        notify(message, self.get_message_key(), target_object=self, url=self.get_notification_url())

    def save(self, *args, **kwargs):
        if self.id:
            changed = False
            for field in self.watch_fields:
                try:
                    new = getattr(self, field)
                    old = getattr(self, self.old_field_format.format(field=field))
                    if new != old:
                        changed = True
                        break
                except AttributeError:
                    # Avoid causing trouble
                    pass

            if changed:
                self.notify("{object} har endret seg.".format(object=self))

        return super(EditMessageMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class EditableMedia(ViewCounterMixin, EditMessageMixin):
    # Metadata
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
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(CommentsMixin, self).save(*args, **kwargs)

