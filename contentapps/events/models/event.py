# -*- coding: utf-8 -*-

import logging
from django.core.urlresolvers import reverse

from ..exceptions import RegistrationAlreadyExists, EventFullException, DeregistrationClosed
from .abstract_event import AbstractEvent
from .eventregistration import EventRegistration


class Event(AbstractEvent):
    """Arrangementer både med og uten påmelding.
    Dukker opp som nyheter på forsiden.
    """

    class Meta:
        verbose_name = "arrangement"
        verbose_name_plural = "arrangement"
        permissions = (
            ("administer", "Can administer models"),
        )
        db_table = "content_event"

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        self._prune_queue()
        EventRegistration.objects.update_lists(self)

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

    def users_attending_emails(self):
        """
        :return: List of attending users emails.
        """
        attending = self.attending_registrations
        return [att.user.email for att in attending]

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
        self._assert_user_allowed_to_register(user)
        return self.add_to_attending_or_waiting_list(user)

    def add_to_attending_or_waiting_list(self, user):
        if self.eventregistration_set.filter(user=user).exists():
            raise RegistrationAlreadyExists(event=self, user=user)

        if not self.is_full():
            return EventRegistration.objects.create_attending_registration(event=self, user=user)
        elif self.has_queue:
            return EventRegistration.objects.create_waiting_registration(event=self, user=user)
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

    def _prune_queue(self):
        """Sletter overflødige registreringer."""
        if not self.registration_required:
            self.eventregistration_set.all().delete()
        elif not self.has_queue:
            self.waiting_registrations.delete()

    def get_registration_url(self):
        return reverse('registration', kwargs={'pk': self.pk})
