# -*- coding: utf-8 -*-

from django.db import models
from content.models import Content

class Nablad(Content):
    pub_date = models.DateField(verbose_name='publisert',  blank=True, null=True, help_text="Publikasjonsdato")
    headline = models.CharField(verbose_name='overskrift', max_length=100, blank=False, help_text="Overskrift på detaljsiden")
    file = models.FileField(upload_to='nabladet', verbose_name='PDF-fil', help_text="Filnavn")
    picture = models.ImageField(upload_to="news_pictures", null=True, blank=True, help_text="Forsidebilde")
    blurb = models.TextField(verbose_name="beskrivelse", blank=True, help_text="Vises på detaljsiden")

    class Meta:
        verbose_name = 'nablad'
        verbose_name_plural = 'nablad'

    def __unicode__(self):
        return self.headline
