# -*- coding: utf-8 -*-

# Modeller for stillingsannonser-appen

from django.db import models
from content.models import Content
from news.models import News

# Det er litt stygt å bruke modeller for YearChoices og RelevantForChoices, men
# det var den enkle måten å få riktige forms i admin på.

class YearChoices(models.Model):
    year = models.IntegerField(blank=False, verbose_name="Klasse", help_text="Klasse: 1, 2, 3, 4 og 5")

    class Meta:
        verbose_name = "Klasse"
        verbose_name_plural = "Klasser"
        permissions = (
            ("can_see_static_models", "Can see static models"),
        )

    def __unicode__(self):
        return u'%s' % (str(self.year))


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
    website = models.CharField(max_length=200, blank=True, verbose_name="Nettside")
    name = models.CharField(verbose_name="navn", max_length=200, blank=False)
    description = models.TextField(verbose_name="beskrivelse", blank=True)

    class Meta:
        verbose_name = "bedrift"
        verbose_name_plural = "bedrifter"

    def __unicode__(self):
        return self.name


class Advert(News):
    company = models.ForeignKey('Company', verbose_name="Bedrift", help_text="Hvilken bedrift stillingen er hos")

    relevant_for_group = models.ManyToManyField(RelevantForChoices, blank=False, verbose_name="Studieretning", help_text="Hvilke studieretninger stillingsannonsen er relevant for")
    relevant_for_year = models.ManyToManyField(YearChoices, blank=False, null=True, verbose_name="Årskull", help_text="Hvilke årskull stillingsannonsen er relevant for")
    tags = models.ManyToManyField(TagChoices, blank=True, verbose_name="Tags", help_text="F.eks. sommerjobb, bergen, kirkenes, olje, konsultering...")

    deadline_date = models.DateTimeField(verbose_name="Frist", blank=True, null=True, help_text="Søknadsfrist")  # Naar frist for soeking er, med klokkeslett

    show_removal_date = models.BooleanField(default=False, help_text="Om fjerningsdato skal vises", verbose_name="Vis fjerningsdato?")  # Hvorvidt removal_date skal vises i stillingsannonsen
    removal_date = models.DateTimeField(verbose_name="Forsvinner", null=True, blank=True, help_text="Når annonsen fjernes, f.eks. samtidig som deadline")  # Naar annonsen skal fjernes, for eksempel samtidig som deadline_date

    info_file = models.FileField(upload_to="stillinger", blank=True, verbose_name="Informasjonsfil", help_text="Informasjon om stillingen")
    antall_stillinger = models.IntegerField(verbose_name="Antall stillinger", blank=True, null=True, help_text="Antall stillinger som tilbys")

    contact_info = models.TextField(blank=True, verbose_name="Kontaktinfo", help_text="Kontaktinformasjon for søkere")

    class Meta:
        verbose_name = "stillingsannonse"
        verbose_name_plural = "stillingsannonser"

    def __unicode__(self):
        return self.headline
