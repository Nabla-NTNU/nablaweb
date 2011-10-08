# -*- coding: utf-8 -*-

# Modeller for stillingsannonser-appen

from django.db import models
from content.models import Content

class Company(Content):
    website = models.CharField(max_length=200, blank=True, verbose_name="Nettside")

class Advert(Content):
    RELEVANT_FOR_CHOICES = ((u'B', u'Biofysikk'), (u'T', u'Teknisk fysikk'), (u'I', u'Industriell matematikk'))
    
    company = models.ForeignKey('Company')
    
    relevant_for = models.CharField(max_length=30, choices=RELEVANT_FOR_CHOICES, blank=False, verbose_name="Relevant for", help_text="Hvem som har interesse av stillingsannonsen") # Hvem som har interesse av aa se stillingsannonsene
    
    deadline_date = models.DateTimeField(verbose_name="Frist") # Naar frist for soeking er, med klokkeslett
    expiry_date = models.DateTimeField(verbose_name="Forsvinner") # Naar annonsen skal fjernes, for eksempel samtidig som deadline_date

    info_file = models.FileField(upload_to="stillinger", blank=True, verbose_name="Informasjonsfil", help_text="Informasjon om stillingen")
    antall_stillinger = models.IntegerField(verbose_name="Antall stillinger", blank=True, null=True)
