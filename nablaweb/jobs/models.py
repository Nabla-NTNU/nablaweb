# -*- coding: utf-8 -*-

# Modeller for stillingsannonser-appen

from django.db import models
from content.models import Content

class RelevantForChoices(models.Model):
    RELEVANT_FOR_CHOICES = ((u'B', u'Biofysikk'), (u'T', u'Teknisk fysikk'), (u'I', u'Industriell matematikk'))
    choice = models.CharField(max_length=50, verbose_name="Valg", help_text='Mulige valg for "relevant for" når man legger til stillingsannonser.')
    
    class Meta:
        verbose_name = 'Mulig valg for "relevant for"'
        verbose_name_plural = 'Mulige valg for "relevant for"'
    
    def __unicode__(self):
        return u'%s' % (self.choice)
        
class TagChoices(models.Model):
    tag = models.CharField(max_length=100, verbose_name="Tags", help_text="Tags for stillingsannonsen. Eksempler: deltid, sommerjobb, fulltid, utlandet, by. Søkbar.")
    
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    def __unicode__(self):
        return u'%s' % (self.tag)

class Company(Content):
    # Headline er bedriftens navn. Body ment for informasjon om bedriften. Lead_paragraph evt. for en liten blurb om bedriften.
    # Website er bedriftens nettside.    
    website = models.CharField(max_length=200, blank=True, verbose_name="Nettside")
    
    class Meta:
        verbose_name = "Bedrift"
        verbose_name_plural = "Bedrifter"

class Advert(Content):
    company = models.ForeignKey('Company')
    
    # relevant_for = models.CharField(max_length=30, choices=RELEVANT_FOR_CHOICES, blank=False, verbose_name="Relevant for", help_text="Hvem som har interesse av stillingsannonsen") # Hvem som har interesse av aa se stillingsannonsene
    relevant_for = models.ManyToManyField(RelevantForChoices)
    tags = models.ManyToManyField(TagChoices)
    
    deadline_date = models.DateTimeField(verbose_name="Frist", blank=True) # Naar frist for soeking er, med klokkeslett
    show_expiry_date = models.BooleanField(default="False") # Hvorvidt expiry_date skal vises i stillingsannonsen
    expiry_date = models.DateTimeField(verbose_name="Forsvinner") # Naar annonsen skal fjernes, for eksempel samtidig som deadline_date

    info_file = models.FileField(upload_to="stillinger", blank=True, verbose_name="Informasjonsfil", help_text="Informasjon om stillingen")
    antall_stillinger = models.IntegerField(verbose_name="Antall stillinger", blank=True, null=True)
    
    contact_info = models.CharField(max_length=1500, blank=True, verbose_name="Kontaktinformasjon", help_text="Kontaktinformasjon for søkere")

    class Meta:
        verbose_name = "Stillingsannonse"
        verbose_name_plural = "Stillingsannonser"
