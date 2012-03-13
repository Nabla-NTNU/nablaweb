# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from pybb.models import PybbProfile

class UserProfile(PybbProfile):
    user = models.OneToOneField(User)
    telephone = models.CharField("Telefon", max_length = 15, blank=True)
    cell_phone = models.CharField("Mobil", max_length = 15, blank=True)
    birthday = models.DateField("Bursdag", blank =True, null=True)
    address = models.CharField("Adresse", max_length = 40, blank = True)
    mail_number = models.CharField("Postnr", max_length = 4, blank = True)
    web_page = models.CharField("Hjemmeside", max_length = 80, blank = True)
    wants_email = models.BooleanField("Motta kullmail", default = True)
    about = models.TextField("Biografi",blank = True)
    ntnu_card_number = models.CharField("NTNU kortnr",max_length = 20, blank = True)
    def __unicode__(self):
        return "< %s profile >" % self.user.username


## Ekstrainformasjon for grupper
class GroupProfile(models.Model):
    group = models.OneToOneField(Group, editable = False)
    leaders = models.ManyToManyField(User, verbose_name ="Ledere", blank=True)
    description = models.TextField(verbose_name = "Beskrivelse",blank = True)
    mail_list = models.EmailField(verbose_name = "Epostliste",blank = True)

    GROUP_TYPES = (
        ('komite', 'Komité'),
        ('kull', 'Kull'),
        ('studprog', 'Studieprogram'),
        ('stilling', 'Stilling'),
        )

    group_type = models.CharField(max_length = 10,blank = True, choices = GROUP_TYPES)

    def __unicode__(self):
        return self.group.name
