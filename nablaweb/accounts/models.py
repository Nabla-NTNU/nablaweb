# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from pybb.models import PybbProfile
from datetime import date

class UserProfile(PybbProfile):
    """ Ekstrainformasjon for brukere. """
    user = models.OneToOneField(User)
    telephone = models.CharField("Telefon", max_length = 15, blank=True)
    cell_phone = models.CharField("Mobil", max_length = 15, blank=True)
    birthday = models.DateField("Bursdag", blank =True, null=True)
    address = models.CharField("Adresse", max_length = 40, blank = True)
    mail_number = models.CharField("Postnr", max_length = 4, blank = True)
    web_page = models.CharField("Hjemmeside", max_length = 80, blank = True)
    wants_email = models.BooleanField("Motta kullmail", default = True)
    about = models.TextField("Biografi",blank = True)
    ntnu_card_number = models.CharField("NTNU kortnr",max_length = 10, blank = True, help_text ="Dette er det 7-10 siffer lange nummeret på baksiden av NTNU-adgangskortet ditt. Det brukes blant annet for å komme inn på bedpresser.")

    def get_class_number(self):
        """ Henter hvilken klasse på fysmat (1-5) brukeren går i. Returnerer 0 hvis brukeren ikke går på fysmat."""
        try:
            return FysmatClass.objects.filter(user = self.user).order_by('starting_year')[0].get_class_number()
        except:
            return 0
     

    def __unicode__(self):
        return "< %s profile >" % self.user.username


class NablaGroup(Group):
    """
    Subklasse av Group som definerer ekstrainformasjon om grupper
    """
    description = models.TextField(verbose_name = "Beskrivelse",blank = True)
    mail_list = models.EmailField(verbose_name = "Epostliste",blank = True)

      

    GROUP_TYPES = (
        ('komite', 'Komité'),
        ('kull', 'Kull'),
        ('studprog', 'Studieprogram'),
        ('komleder', 'Komitéleder'),
        ('styremedlm', 'Styremedlem'),
        ('stilling', 'Stilling'),
        )

    group_type = models.CharField(max_length = 10,blank = True, choices = GROUP_TYPES)


class Committee(NablaGroup):
    class Meta:
        abstract = True
    objects = NablaGroup.objects.filter(group_type = 'komite')

class GroupLeader(NablaGroup):
      """ Gruppe for en person, for eksempel komiteledere og lignende """
      leads = models.OneToOneField(NablaGroup, related_name = "leader")

class FysmatClass(NablaGroup):
    """ Gruppe for kull """
    class Meta:
        verbose_name = "Kull"
        verbose_name_plural = "Kull"

    starting_year = models.CharField("År startet", max_length = 4, unique = True)

    def get_class_number(self):
        now = date.today()
        return now.year - int(self.starting_year) + int(now.month>6)
