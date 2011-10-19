# -*- coding: utf-8 -*-

# Modeller for kom-appen

from django.db import models
from content.models import Content
from accounts.models import UserProfile, GroupProfile

class ComPage:
    # Gruppemedlemmene hentes fra gruppen med samme navn som Committee-klassen sin name gjort om til lowercase og space gjort om til underscore
    # Leder hentes fra samme sted
    com = models.ForeignKey('accounts.GroupProfile')
    description = models.CharField(max_length=2000, verbose_name="Beskrivelse av komiteen", help_text="Denne beskrivelsen utgjør teksten som står på gruppens side.")
    
    # Egne gruppenyheter?

class GroupMember(UserProfile):
    # Må automatisk lages når en bruker blir med i komité-gruppen
    story = models.CharField(max_length=2000, verbose_name="Beskrivelse av gruppemedlemmet", help_text="Ansvarsområde og lignende")
    joined_date = models.DateField(verbose_name="Ble med", help_text="Datoen personen ble med i komiteen")
