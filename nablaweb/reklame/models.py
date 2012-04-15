# -*- coding: utf-8 -*-

from django.db import models
from image_cropping.fields import ImageRatioField, ImageCropField

class Reklame(models.Model):
    advertiser = models.CharField(verbose_name="reklamør", max_length=200, blank=False)
    link = models.CharField(verbose_name="lenke", max_length=200, blank=False)

    picture = ImageCropField(upload_to="ad_pictures", null=True, blank=True)
    cropping = ImageRatioField('picture', '362x200', verbose_name="Beskjæring")
    
    created_date = models.DateTimeField(verbose_name="Publiseringsdato", auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name="Opprettet av", related_name="%(class)s_created", editable=False, blank=True, null=True)
    last_changed_date = models.DateTimeField(verbose_name="Redigeringsdato", auto_now=True, null=True)
    last_changed_by = models.ForeignKey(User, verbose_name="Endret av", related_name="%(class)s_edited", editable=False, blank=True, null=True)
    
    def __unicode__(self):
        retstring = self.advertiser + "_" + self.id
        return retstring

    def has_been_edited(self):
        return abs((self.last_changed_date - self.created_date).seconds) > 1
