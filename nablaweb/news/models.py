# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from content.models import Content


class News(Content):
    headline = models.CharField(verbose_name="tittel", max_length=100, blank=False)
    lead_paragraph = models.TextField(verbose_name="ingress", blank=True)
    body = models.TextField(verbose_name="innhold", blank=True)

    class Meta:
        verbose_name = "nyhet"
        verbose_name_plural = "nyheter"

    def __unicode__(self):
        return self.headline
