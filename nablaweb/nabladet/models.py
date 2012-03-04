# -*- coding: utf-8 -*-

from django.db import models
from news.models import News


class Nablad(News):
    pub_date = models.DateField(verbose_name='publisert',  blank=True, null=True, help_text="Publikasjonsdato")
    file = models.FileField(upload_to='nabladet', verbose_name='PDF-fil', help_text="Filnavn")

    class Meta:
        verbose_name = 'nablad'
        verbose_name_plural = 'nablad'

    def __unicode__(self):
        return self.headline
