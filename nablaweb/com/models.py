# -*- coding: utf-8 -*-

# Modeller for com-appen

from django.db import models
from news.models import News
from django.contrib.auth.models import Group, User
from django.template.defaultfilters import slugify
from django.utils.encoding import force_unicode

class ComPage(models.Model):
    # Gruppemedlemmene hentes fra gruppen med samme navn som Committee-klassen sin name gjort om til lowercase og space gjort om til underscore
    # Leder hentes fra samme sted
    com = models.ForeignKey(Group)

    description = models.TextField(verbose_name="Beskrivelse", help_text="Teksten på komitésiden", blank=True)
    slug = models.CharField(verbose_name="Slug til URL-er", max_length=50, blank=False, unique=True, editable=False)
    
    last_changed_date = models.DateTimeField(verbose_name="Sist redigert", auto_now=True, null=True)
    last_changed_by = models.ForeignKey(User, verbose_name="Sist endret av", related_name="%(class)s_edited", editable=False, blank=True, null=True)

    def __unicode__(self):
        return force_unicode(self.com.name)

    def has_been_edited(self):
        return self.last_changed_by is not None
        
    def get_canonical_name(self):
        return slugify(self.__unicode__())
    
    def get_absolute_url(self):
        return "/komite/" + self.get_canonical_name()
        
    def save(self, *args, **kwargs):
        self.slug = self.get_canonical_name()
        super(ComPage, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "komiteside"
        verbose_name_plural = "komitesider"
        
    # Egne gruppenyheter?

class ComMembership(models.Model):
    user = models.ForeignKey('auth.User')
    com = models.ForeignKey('auth.Group', verbose_name="Komité")
    story = models.TextField(blank=True, verbose_name="Beskrivelse", help_text="Ansvarsområde eller lignende")
    joined_date = models.DateField(blank=True, null=True, verbose_name="Ble med", help_text="Dato personen ble med i komiteen")
    left_date = models.DateField(blank=True, null=True, verbose_name="Sluttet", help_text="Dato personen sluttet i komiteen")
    is_active = models.BooleanField(blank=False, null=False, verbose_name="Aktiv?", default=True)

    def save(self, *args, **kwargs):
        self.com.user_set.add(self.user)
        super(ComMembership, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.com.user_set.remove(self.user)
        super(ComMembership, self).delete(*args, **kwargs)
    
    def __unicode__(self):
        return force_unicode(self.user.username)
        
    class Meta:
        verbose_name = "komitemedlem"
        verbose_name_plural = "komitemedlemmer"
