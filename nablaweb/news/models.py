# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from content.models import Content


class News(Content):
    picture = models.ImageField(upload_to="news_pictures", null=True, blank=True, help_text="Bredde 620px er optimalt")
    headline = models.CharField(verbose_name="tittel", max_length=100, blank=False)
    lead_paragraph = models.TextField(verbose_name="ingress", blank=True, help_text="Vises på forsiden og i artikkelen")
    body = models.TextField(verbose_name="brødtekst", blank=True, help_text="Vises kun i artikkelen")

    class Meta:
        verbose_name = "nyhet"
        verbose_name_plural = "nyheter"

    def __unicode__(self):
        return self.headline
