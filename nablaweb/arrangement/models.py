# -*- coding: utf-8 -*-

# arrangement/models.py


from django.db import models
from django.contrib.auth.models import User
from innhold.models import SiteContent
import datetime


class Event(SiteContent):
    class Meta(SiteContent.Meta):
        verbose_name_plural = "arrangement"

    # Indikerer hvem som står bak arrangementet.
    # Dette feltet er valgfritt.
    organizer = models.CharField(max_length=100, blank=True)

    # Hvor arrangementet foregår.
    location = models.CharField(max_length=100, blank=False)

    # Når arrangementet starter.
    event_start = models.DateTimeField(null=True, blank=False)

    # Når arrangementet slutter.
    # Dette feltet er valgfritt.
    # Datoen er ikke tidligere enn event_start.
    event_end = models.DateTimeField(null=True, blank=True)

    # Frist for å melde seg på arrangementet.
    # Dette feltet er valgfritt.
    # At dette feltet er satt er ekvivalent med at arrangementet krever påmelding.
    # Datoen er ikke senere enn event_start.
    registration_deadline = models.DateTimeField(null=True, blank=True)

    # Frist for å melde seg av arrangementet.
    # Dette feltet er valgfritt.
    # Dette feltet er bare satt hvis registration_deadline er satt.
    # Datoen er ikke senere enn event_start.
    deregistration_deadline = models.DateTimeField(null=True, blank=True)

    # Hvor mange plasser arrangementet har.
    # Dette feltet er satt hvis og bare hvis registration_deadline er satt.
    # Antall plasser er et heltall ikke mindre enn null.
    places = models.PositiveIntegerField(null=True, blank=True)

    # Om arrangementet har venteliste.
    # Dette feltet er valgfritt.
    # Dette feltet er bare satt hvis registration_deadline er satt.
    has_queue = models.NullBooleanField(null=True, blank=True)

    def __unicode__(self):
        return u'%s, %s' % (self.headline, self.event_start.strftime('%d/%m/%y'))

    def free_places(self):
        return self.places - self.eventregistration_set.count()

    def is_full(self):
        return self.free_places() <= 0

    def users_attending(self):
        return min(self.eventregistration_set.count(), self.places)

    def users_waiting(self):
        return -min(self.free_places(), 0)

    def is_attending(self, user):
        pass

    def registration_required(self):
        return self.registration_deadline is not None

    def has_waiting_list(self):
        return self.has_queue is not None

    def register_user(self, user):
        if self.registration_deadline is None:
            return u"Ingen påmelding."
        elif datetime.datetime.now() > self.registration_deadline:
            return u"Påmeldingen har stengt."
        elif self.is_full() and self.has_queue is False:
            return u"Fullt."
        registration = self.eventregistration_set.filter(person=user)
        if registration:
            registration = registration[0]
        else:
            registration = EventRegistration(
                event=self,
                person=user,
                place=self.eventregistration_set.count()+1,
                )
            registration.save()
        if registration.place <= self.places:
            return u"Du er påmeldt."
        else:
            return u"Du står på venteliste."

    def test_event_fields(self):
        assert isinstance(self.location, str) or isinstance(self.location, unicode)
        assert self.location != '' and self.location != u''

        assert self.event_start is not None
        assert isinstance(self.event_start, datetime.datetime)

        if self.event_end is not None:
            assert isinstance(self.event_end, datetime.datetime)
            assert self.event_end >= self.event_start

        if self.registration_deadline is not None:
            assert isinstance(self.registration_deadline, datetime.datetime)
            assert self.registration_deadline <= self.event_start 
            assert isinstance(self.places, int) or isinstance(self.places, long)
            assert self.places >= 0
            assert isinstance(self.has_queue, bool)
        else:
            assert self.places is None
            assert self.deregistration_deadline is None
            assert self.has_queue is None

        if self.deregistration_deadline is not None:
            assert isinstance(self.deregistration_deadline, datetime.datetime)
            assert self.deregistration_deadline <= self.event_start
            assert self.deregistration_deadline >= self.registration_deadline

        if self.has_queue is not None:
            assert isinstance(self.has_queue, bool)


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
