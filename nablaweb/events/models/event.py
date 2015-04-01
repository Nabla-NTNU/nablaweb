# -*- coding: utf-8 -*-

import logging

from ..exceptions import *
from .abstract_event import AbstractEvent


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

    @property
    def registrations_manager(self):
        from .eventregistration import EventRegistration
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
        from .eventregistration import EventRegistration

        if not self.is_full():
            return EventRegistration.create_attending_registration(event=self, user=user)
        elif self.has_queue:
            return EventRegistration.create_waiting_registration(event=self, user=user)
        else:
            raise EventFullException(event=self, user=user)

    def deregister_user(self, user):
        """Melder brukeren av arrangementet."""
        from .eventregistration import EventRegistration
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
