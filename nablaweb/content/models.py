# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from image_cropping.fields import ImageRatioField, ImageCropField
from model_utils.managers import InheritanceManager


class Content(models.Model):
    # Metadata
    created_date = models.DateTimeField(verbose_name="Publiseringsdato", auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name="Opprettet av", related_name="%(class)s_created", editable=False, blank=True, null=True)
    last_changed_date = models.DateTimeField(verbose_name="Redigeringsdato", auto_now=True, null=True)
    last_changed_by = models.ForeignKey(User, verbose_name="Endret av", related_name="%(class)s_edited", editable=False, blank=True, null=True)

    # Bildeopplasting med resizing og cropping
    picture = ImageCropField(upload_to="news_pictures", null=True, blank=True, help_text="Bilder som er større enn 770x250 px ser best ut. Du kan beskjære bildet etter opplasting.")
    cropping = ImageRatioField('picture', '770x250', verbose_name="Beskjæring")

    # django-model-utils gjør det mulig for News å hente Event og News-objekter i samme liste.
    objects = InheritanceManager()

    class Meta:
        abstract = True

    def has_been_edited(self):
        return abs((self.last_changed_date - self.created_date).seconds) > 1

    def get_absolute_url(self):
        return "Content sin get_absolute_url blir kjørt. Noe er galt."
        raise NotImplementedError("get_absolute_url not implemented in the subclass " + self.__class__.__name__)
