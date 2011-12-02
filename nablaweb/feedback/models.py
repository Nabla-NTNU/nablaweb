# -*- coding: utf-8 -*-

from django.db import models

class Feedback(models.Model):

    created_date = models.DateTimeField(verbose_name="Dato opprettet", auto_now_add=True, null=True, editable=False)
    
    headline = models.CharField(verbose_name="Tittel", max_length=128, blank=False)
    created_by = models.CharField(verbose_name="Opprettet av", max_length=64, blank=False)
    body = models.TextField(verbose_name="Innhold", blank=False)
    
    def __unicode__(self):
        return u'"%s" av %s' % (self.headline,self.created_by)
        
