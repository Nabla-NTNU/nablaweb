# -*- coding: utf-8 -*-

# Modeller for stillingsannonser-appen

from django.db import models
from news.models import News
from content.models import Content

# Det er litt stygt å bruke modeller for YearChoices og RelevantForChoices, men
# det var den enkle måten å få riktige forms i admin.

class YearChoices(models.Model):
    year = models.IntegerField(blank=False, verbose_name="Klasse", help_text="Klasse: 1, 2, 3, 4 og 5")
    
    class Meta:
        verbose_name = "Klasse"
        verbose_name_plural = "Klasser"
        permissions = (
            ("can_see_static_models", "Can see static models"),
        )
    
    def __unicode__(self):
        return u'%s' %(str(self.year))

class RelevantForChoices(models.Model):
    studieretning = models.CharField(max_length=50, verbose_name="Valg", help_text='Mulige valg for "relevant for" når man legger til stillingsannonser.')
    
    class Meta:
        verbose_name = 'Mulig valg for "relevant for"'
        verbose_name_plural = 'Mulige valg for "relevant for"'
    
    def __unicode__(self):
        return u'%s' % (self.studieretning)
        
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
    name = models.CharField(verbose_name="navn", max_length=200, blank=False)
    description = models.TextField(verbose_name="beskrivelse", blank=True)
    picture = models.ImageField(upload_to="company_pictures", null=True, blank=True)
    
    class Meta:
        verbose_name = "bedrift"
        verbose_name_plural = "bedrifter"

class Advert(Content):
    company = models.ForeignKey('Company')
    picture = models.ImageField(upload_to="job_advert_pictures", null=True, blank=True)

    headline = models.CharField(max_length=200, blank=False, verbose_name="tittel")
    lead_paragraph = models.TextField(verbose_name="ingress", blank=True)
    body = models.TextField(verbose_name="beskrivelse", blank=True)
    
    relevant_for_group = models.ManyToManyField(RelevantForChoices)
    relevant_for_year = models.ManyToManyField(YearChoices, blank=True, null=True, verbose_name="Årskull", help_text="Hvilke klasser stillingsannonsen er relevant for")
    tags = models.ManyToManyField(TagChoices)
    
    deadline_date = models.DateTimeField(verbose_name="Frist", blank=True) # Naar frist for soeking er, med klokkeslett
    show_expiry_date = models.BooleanField(default="False") # Hvorvidt expiry_date skal vises i stillingsannonsen
    expiry_date = models.DateTimeField(verbose_name="Forsvinner") # Naar annonsen skal fjernes, for eksempel samtidig som deadline_date

    info_file = models.FileField(upload_to="stillinger", blank=True, verbose_name="Informasjonsfil", help_text="Informasjon om stillingen")
    antall_stillinger = models.IntegerField(verbose_name="Antall stillinger", blank=True, null=True)
    
    contact_info = models.CharField(max_length=1500, blank=True, verbose_name="Kontaktinformasjon", help_text="Kontaktinformasjon for søkere")

    class Meta:
        verbose_name = "stillingsannonse"
        verbose_name_plural = "stillingsannonser"

    def __unicode__(self):
        return self.headline
