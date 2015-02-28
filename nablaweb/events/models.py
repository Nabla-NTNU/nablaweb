# -*- coding: utf-8 -*-

import logging

from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django.template import loader, Context

from urlparse import urlparse
from datetime import datetime
from news.models import News
from .exceptions import *


class AbstractEvent(News):
    """
    Abstrakt modell som definerer det som er felles
    for Event og BedPres.
    """
    short_name = models.CharField(
        verbose_name="kort navn",
        max_length=20,
        blank=True,
        null=True,
        help_text="Brukes på steder hvor det ikke er plass til å skrive hele overskriften, for eksempel kalenderen.")
    organizer = models.CharField(
        verbose_name="organisert av",
        max_length=100,
        blank=True,
        help_text="Den som står bak arrangementet")
    location = models.CharField(
        verbose_name=u"sted",
        max_length=100,
        blank=False)
    event_start = models.DateTimeField(
        verbose_name="start",
        null=True,
        blank=False)
    event_end = models.DateTimeField(
        verbose_name="slutt",
        null=True,
        blank=True)
    facebook_url = models.CharField(
        verbose_name="facebook-url",
        blank=True,
        max_length=100,
        help_text="URL-en til det tilsvarende arrangementet på Facebook")

    # Medlemsvariabler som har med påmelding å gjøre. De fleste er kun relevant
    # hvis registration_required er satt til True.
    registration_required = models.BooleanField(
        verbose_name="påmelding",
        default=False,
        null=False,
        blank=False)
    registration_deadline = models.DateTimeField(
        verbose_name="påmeldingsfrist",
        null=True,
        blank=True)
    registration_start = models.DateTimeField(
        verbose_name="påmelding åpner",
        null=True,
        blank=True)
    deregistration_deadline = models.DateTimeField(
        verbose_name="avmeldingsfrist",
        null=True,
        blank=True)
    places = models.PositiveIntegerField(
        verbose_name="antall plasser",
        null=True,
        blank=True)
    has_queue = models.NullBooleanField(
        verbose_name="har venteliste",
        null=True,
        blank=True,
        help_text=("Om ventelisten er på, vil det være mulig å melde seg på selv om arrangementet er fullt. "
                   "De som er i ventelisten vil automatisk bli påmeldt etter hvert som plasser blir ledige.")
    )
    open_for = models.ManyToManyField(
        Group,
        verbose_name="Åpen for",
        blank=True,
        null=True,
        help_text=("Hvilke grupper som får lov til å melde seg på arrangementet. "
                   "Hvis ingen grupper er valgt er det åpent for alle.")
    )

    class Meta:
        abstract = True

    def allowed_to_attend(self, user):
        """Indikerer om en bruker har lov til å melde seg på arrangementet"""
        return (not self.open_for.exists()) or self.open_for.filter(user=user).exists()

    def has_started(self):
        return self.event_start < datetime.now()

    def has_finished(self):
        return self.event_end and self.event_end < datetime.now()

    def registration_has_started(self):
       return self.registration_required and self.registration_start < datetime.now()

    def registration_open(self):
        return self.registration_has_started() and datetime.now() < self.registration_deadline

    def deregistration_closed(self):
        return self.deregistration_deadline and (self.deregistration_deadline < datetime.now())

    def __unicode__(self):
        return u'%s, %s' % (self.headline, self.event_start.strftime('%d.%m.%y'))

    def get_short_name(self):
        """Henter short_name hvis den finnes, og kutter av enden av headline hvis ikke."""
        if self.short_name:
            return self.short_name
        if len(self.headline) <= 19:
            return self.headline
        return self.headline[0:18].capitalize() + '...'


class Event(AbstractEvent):
    """Arrangementer både med og uten påmelding.
    Dukker opp som nyheter på forsiden.
    """

    class Meta:
        verbose_name = "arrangement"
        verbose_name_plural = "arrangement"
        permissions = (
            ("administer", "Can administer events"),
        )

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        self._prune_queue()

    def delete(self, *args, **kwargs):
        self.eventregistration_set.all().delete()
        super(Event, self).delete(*args, **kwargs)

    def clean(self):
        self.clean_facebook_url()

    def clean_facebook_url(self):
        """Verifiserer formen på facebook-urlen, og endrer den hvis den er feil."""
        parsed = urlparse(self.facebook_url)
        noscheme = parsed.netloc + parsed.path
        self.facebook_url = 'http' + '://' + noscheme.replace("http://", "").replace("https://", "")

        if self.facebook_url == "http://":
            self.facebook_url = ""

    @property
    def registrations_manager(self):
        return EventRegistration.get_manager_for(self)

    @property
    def waiting_registrations(self):
        return self.registrations_manager.waiting_ordered()

    @property
    def attending_registrations(self):
        return self.registrations_manager.attending_ordered()

    def free_places(self):
        """Returnerer antall ledige plasser.

        dvs antall plasser som umiddelbart gir brukeren en garantert plass, og ikke bare
        ventelisteplass.
        Returnerer 0 hvis self.places er None.
        """
        try:
            return max(self.places - self.users_attending(), 0)
        except TypeError:
            return 0

    def is_full(self):
        return self.free_places() == 0

    def users_attending(self):
        """Returnerer antall brukere som er påmeldt."""
        return self.attending_registrations.count()

    def users_waiting(self):
        """Returnerer antall brukere som står på venteliste."""
        return self.waiting_registrations.count()

    def percent_full(self):
        """Returnerer hvor mange prosent av plassene som er tatt."""
        try:
            return min(self.users_attending() * 100 / int(self.places), 100)
        except TypeError:
            return 0
        except ZeroDivisionError:
            return 100

    def is_registered(self, user):
        return self.eventregistration_set.filter(user=user).exists()

    def is_attending(self, user):
        return self.attending_registrations.filter(user=user).exists()

    def is_waiting(self, user):
        return self.waiting_registrations.filter(user=user).exists()

    def get_attendance_list(self):
        return [e.user for e in self.attending_registrations]

    def get_waiting_list(self):
        return [e.user for e in self.waiting_registrations]

    def register_user(self, user):
        """Forsøker å melde brukeren på arrangementet."""
        self._raise_exceptions_if_not_allowed_to_register(user)
        return self.add_to_attending_or_waiting_list(user)

    def _raise_exceptions_if_not_allowed_to_register(self, user):
        if not self.registration_required:
            raise RegistrationNotRequiredException(event=self, user=user)
        elif not self.registration_open():
            raise RegistrationNotOpen(event=self, user=user)
        elif not self.allowed_to_attend(user):
            raise RegistrationNotAllowed(event=self, user=user)

    def add_to_attending_or_waiting_list(self, user):
        if self.eventregistration_set.filter(user=user).exists():
            raise RegistrationAlreadyExists(event=self, user=user)

        if not self.is_full():
            return EventRegistration.create_attending_registration(event=self, user=user)
        elif self.has_queue:
            return EventRegistration.create_waiting_registration(event=self, user=user)
        else:
            raise EventFullException(event=self, user=user)

    def deregister_user(self, user):
        """Melder brukeren av arrangementet."""
        regs = self.eventregistration_set
        if self.deregistration_closed():
            raise DeregistrationClosed(event=self, user=user)
        try:
            reg = regs.get(user=user)
            reg.delete()
        except EventRegistration.DoesNotExist:
            logger = logging.getLogger(__name__)
            logger.info('Attempt to deregister user from non-existent event.')
        else:
            self.update_lists()

    def update_lists(self):
        self._fix_list_numbering()
        self._move_waiting_to_attending()

    def _fix_list_numbering(self):
        attending_regs = self.attending_registrations
        for n, reg in enumerate(attending_regs, start=1):
            reg.number = n
            reg.save()

        waiting_regs = self.waiting_registrations
        for n, reg in enumerate(waiting_regs, start=1):
            reg.number = n
            reg.save()

    def _move_waiting_to_attending(self):
        if self.registration_open() and not self.has_started():
            while self.free_places() and self.waiting_registrations.count():
                reg = self.registrations_manager.first_on_waiting_list()
                reg.set_attending_and_send_email()
            self._fix_list_numbering()

    def _prune_queue(self):
        """Sletter overflødige registreringer."""
        if not self.registration_required:
            self.eventregistration_set.all().delete()
        elif not self.has_queue:
            self.waiting_registrations.delete()


class EventRegistration(models.Model):
    """Modell for påmelding på arrangementer.

    Inneholder både påmeldinger og venteliste.
    For ventelistepåmelding er attending satt til False og førstmann på ventelista har number=1.
    """

    event = models.ForeignKey(
        Event,
        blank=False,
        null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='bruker',
        blank=False,
        null=True)
    date = models.DateTimeField(
        verbose_name="Påmeldingsdato",
        auto_now_add=True,
        null=True)
    number = models.PositiveIntegerField(
        verbose_name='kønummer',
        blank=True,
        null=True,
        help_text='Kønummer som tilsvarer plass på ventelisten/påmeldingsrekkefølge.')
    attending = models.BooleanField(
        verbose_name='har plass',
        default=True,
        blank=False,
        null=False,
        help_text="Hvis denne er satt til sann har man en plass på arrangementet ellers er det en ventelisteplass.")

    class Meta:
        verbose_name = 'påmelding'
        verbose_name_plural = 'påmeldte'
        unique_together = (("event", "user"), ("event", "user", "number", "attending"))

    def __unicode__(self):
        return u'%s, %s is %s, place: %s' % (self.event,
                                             self.user,
                                             "Attending" if self.attending else "Waiting",
                                             self.number)

    @classmethod
    def create_attending_registration(cls, event, user):
        attending = True
        number = event.users_attending()+1
        return cls.objects.create(event=event, user=user, attending=attending, number=number)

    @classmethod
    def create_waiting_registration(cls, event, user):
        attending = False
        number = event.users_waiting()+1
        return cls.objects.create(event=event, user=user, attending=attending, number=number)

    @classmethod
    def get_manager_for(cls, event):
        """Henter en manager for en gitt event."""
        return RelatedEventRegistrationManager(event)

    @property
    def waiting(self):
        """Indikerer om det er en ventelisteplass."""
        return not self.attending

    def waiting_list_place(self):
        """Returnerer hvilken plass man har på ventelisten gitt at man er på ventelisten."""
        return self.number if self.waiting else None

    def set_attending_if_waiting(self):
        """Flytter en bruker fra ventelisten til påmeldte hvis ikke allerede påmeldt."""
        if not self.attending:
            self.number = self.event.users_attending()+1
            self.attending = True
            self.save()

    def set_attending_and_send_email(self):
        self.set_attending_if_waiting()
        self._send_moved_to_attending_email()

    def _send_moved_to_attending_email(self):
        if self.user.email:
            subject = u'Påmeldt %s' % self.event.headline
            template = loader.get_template("events/moved_to_attending_email.txt")
            message = template.render(Context({'event': self, 'name': self.user.get_full_name()}))
            self.user.email_user(subject, message)


class RelatedEventRegistrationManager(models.Manager):

    def __init__(self, event):
        self.event = event

    def get_queryset(self):
        return EventRegistration.objects.filter(event=self.event)

    def waiting(self):
        return self.get_queryset().filter(attending=False)

    def waiting_ordered(self):
        return self.waiting().order_by('number')

    def attending(self):
        return self.get_queryset().filter(attending=True)

    def attending_ordered(self):
        return self.attending().order_by('number')

    def first_on_waiting_list(self):
        """Hente førstemann på ventelista."""
        return self.waiting_ordered()[0]
