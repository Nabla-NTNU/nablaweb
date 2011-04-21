# -*- coding: utf-8 -*-

# arrangement/models.py

from django.db import models
from django.contrib.auth.models import User
from innhold.models import SiteContent

class Event(SiteContent):
    class Meta:
        verbose_name_plural = "arrangement"

    organizer = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=False)

    event_start = models.DateTimeField(null=True, blank=False)
    event_end = models.DateTimeField(null=True, blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    deregistration_deadline = models.DateTimeField(null=True, blank=True)

    places = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        return u'%s, %s' % (self.headline, self.event_start.strftime('%d/%m/%y'))

    def free_places(self):
        return self.places - self.eventregistration_set.count()

    def is_full(self):
        return self.free_places() <= 0

    def is_attending(self, user):
        pass

    def registration_required(self):
        if self.registration_deadline is not None:
            return True
        return False


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, blank=False, null=True)
    person = models.ForeignKey(User, blank=False, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    place = models.PositiveIntegerField(blank=False, null=True)


class NoShowDot(models.Model):
    event = models.ForeignKey(Event)
    person = models.ForeignKey(User)

    def __unicode__(self):
        return u'NoShowDot: %s, %s' % (self.event, self.person)
