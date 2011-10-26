# -*- coding: utf-8 -*-

# Modeller for kom-appen

from django.db import models
from content.models import Content
from accounts.models import UserProfile, GroupProfile

class ComPage(models.Model):
    # Gruppemedlemmene hentes fra gruppen med samme navn som Committee-klassen sin name gjort om til lowercase og space gjort om til underscore
    # Leder hentes fra samme sted
    com = models.ForeignKey('accounts.GroupProfile')

    description = models.TextField(verbose_name="Beskrivelse", help_text="Teksten på komitésiden", blank=True)
    
    last_changed_date = models.DateTimeField(verbose_name="Sist redigert", auto_now=True, null=True)
    last_changed_by = models.ForeignKey(UserProfile, verbose_name="Sist endret av", related_name="%(class)s_edited", editable=False, blank=True, null=True)

    def __unicode__(self):
        return self.com.group.name

    def has_been_edited(self):
        return self.last_changed_by is not None
    
    class Meta:
        verbose_name = "Komitéside"
        verbose_name_plural = "Komitésider"
        
    # Egne gruppenyheter?

class ComMember(models.Model):
    # Må automatisk lages når en bruker blir med i komité-gruppen
    user = models.ForeignKey('accounts.UserProfile')
    com = models.ForeignKey('ComPage')
    story = models.TextField(verbose_name="Beskrivelse av gruppe-medlemmet", help_text="Ansvarsområde og lignende")
    joined_date = models.DateField(verbose_name="Ble med", help_text="Datoen personen ble med i komiteen")
    
    class Meta:
        verbose_name = "Komitémedlem"
        verbose_name_plural = "Komitémedlemmer"
