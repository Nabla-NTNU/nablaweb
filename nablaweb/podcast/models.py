# -*- coding: utf-8 -*-

from django.db import models

class Podcast(models.Model):
    title = models.CharField(verbose_name='tittel', max_length=200, blank=False)
    description = models.TextField(verbose_name='beskrivelse', help_text='Tekst. Man kan her bruke <a href="http://en.wikipedis.org/wiki/Markdown\"target=\"_blank\">markdown</a> for å formatere teksten.', blank=True)
    pub_date = models.DateTimeField(verbose_name='publisert', blank=False, null=True, help_text='Publikasjonsdato')
    file = models.FileField(upload_to='podcast', blank=False, verbose_name='lydfil', help_text='Filformat: MP3')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Skråttcast'
        verbose_name_plural = 'Skråttcast'
#        ordering = ('-pub_date')
