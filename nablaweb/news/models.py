# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    created_date = models.DateTimeField(verbose_name="Publiseringsdato", auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name="Opprettet av", related_name="%(class)s_created", editable=False, blank=False, null=True)
    last_changed_date = models.DateTimeField(verbose_name="Redigeringsdato", auto_now=True, null=True)
    last_changed_by = models.ForeignKey(User, verbose_name="Endret av", related_name="%(class)s_edited", editable=False, blank=True, null=True)

    headline = models.CharField(verbose_name="tittel", max_length=100, blank=False)
    lead_paragraph = models.TextField(verbose_name="ingress", blank=True)
    body = models.TextField(verbose_name="innhold", blank=True)

    class Meta:
        verbose_name = "nyhet"
        verbose_name_plural = "nyheter"

    def __unicode__(self):
        return self.headline

    def has_been_edited(self):
        return self.last_changed_by is not None
