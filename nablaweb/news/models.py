# -*- coding: utf-8 -*-


from django.db import models
from content.models import Content


class News(Content):

    # Tekstinnhold
    headline = models.CharField(verbose_name="tittel", max_length=100, blank=False)
    lead_paragraph = models.TextField(verbose_name="ingress", blank=True, help_text="Vises på forsiden og i artikkelen")
    body = models.TextField(verbose_name="brødtekst", blank=True, help_text="Vises kun i artikkelen")

    def correct_picture(self): return self.picture
    def correct_cropping(self): return self.cropping

    class Meta:
        verbose_name = "nyhet"
        verbose_name_plural = "nyheter"
    
    @property
    def as_child_class(self):
        if hasattr(self, 'advert'):
            return self.advert
        elif hasattr(self, 'bedpres'):
            return self.bedpres

    def __unicode__(self):
        return self.headline
