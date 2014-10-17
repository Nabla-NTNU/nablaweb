# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment
import datetime
import os.path

class Podcast(models.Model):
    title = models.CharField(verbose_name='tittel', max_length=200, blank=False)
    description = models.TextField(verbose_name='beskrivelse', help_text='Tekst. Man kan her bruke <a href="http://en.wikipedis.org/wiki/Markdown\"target=\"_blank\">markdown</a> for å formatere teksten.', blank=True)
    pub_date = models.DateTimeField(verbose_name='publisert', blank=False, null=True, help_text='Publikasjonsdato')
    file = models.FileField(upload_to='podcast', blank=False, verbose_name='lydfil', help_text='Filformat: MP3')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Skråttcast'
        verbose_name_plural = 'Skråttcast'
#        ordering = ('-pub_date')
