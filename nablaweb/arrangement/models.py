#!/usr/bin/env python
# -*- coding: utf-8 -*-

# arrangement/models.py

from django.db import models
from django.contrib.auth.models import User
from innhold.models import SiteContent

class Event(SiteContent):
    """class Event(models.Model)"""

    class Meta:
        verbose_name_plural = "arrangement"

    event_type = models.CharField(max_length=32)
    alternative_id = models.CharField(max_length=32, blank=True)
    permissions_string = models.CharField(max_length=80, blank=True)

    organizer = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=False)

    event_start = models.DateTimeField(null=True, blank=False)
    event_end = models.DateTimeField(null=True, blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    deregistration_deadline = models.DateTimeField(null=True, blank=True)

    places = models.PositiveIntegerField(null=True, blank=True)
    attending_users = models.ManyToManyField(User, related_name='events_attending', null=True, blank=True)
    waiting_list = models.ManyToManyField(User, related_name='events_waiting', null=True, blank=True)

    def __unicode__(self):
        return u'%s, %s' % (self.headline, self.event_start.strftime('%d/%m/%y'))

    def free_places(self):
        return self.places - len(self.attending_users.all())

    def is_full(self):
        return self.free_places() == 0

    def is_attending(self, user):
        return user in self.attending_users.all()

class NoShowDot(models.Model):
    event = models.ForeignKey(Event)
    person = models.ForeignKey(User)

    def __unicode__(self):
        return u'NoShowDot: %s, %s' % (self.event, self.person)
