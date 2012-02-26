# -*- coding: utf-8 -*-

# Modeller for com-appen

from django.db import models
from news.models import News
from django.contrib.auth.models import Group, User

class ComPage(models.Model):
    # Gruppemedlemmene hentes fra gruppen med samme navn som Committee-klassen sin name gjort om til lowercase og space gjort om til underscore
    # Leder hentes fra samme sted
    com = models.ForeignKey(Group)

    description = models.TextField(verbose_name="Beskrivelse", help_text="Teksten på komitésiden", blank=True)
    
    last_changed_date = models.DateTimeField(verbose_name="Sist redigert", auto_now=True, null=True)
    last_changed_by = models.ForeignKey(User, verbose_name="Sist endret av", related_name="%(class)s_edited", editable=False, blank=True, null=True)
    
    def __unicode__(self):
        return self.com.name

    def has_been_edited(self):
        return self.last_changed_by is not None
    
    class Meta:
        verbose_name = "komitéside"
        verbose_name_plural = "komitésider"
        
    # Egne gruppenyheter?

class ComMembership(models.Model):
    # Må automatisk lages når en bruker blir med i komité-gruppen
    user = models.ForeignKey('auth.User')
    com = models.ForeignKey('auth.Group', verbose_name="Komité")
    story = models.TextField(verbose_name="Beskrivelse", help_text="Ansvarsområde eller lignende")
    joined_date = models.DateField(verbose_name="Ble med", help_text="Dato personen ble med i komiteen")

    #self.com.com.user_set.add(self.user.user_id)
    
#    def __init__(self):
#        super(ComMembership, self).__init__(*args, **kwargs)
#        self.com.user_set.add(self.user.user_id)
#        print(self.user.username)
    
    def __del__(self): # Må fjerne brukeren fra gruppen når ComMembership-objektet slettes
        pass
    
    def __unicode__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "komitémedlem"
        verbose_name_plural = "komitémedlemmer"
