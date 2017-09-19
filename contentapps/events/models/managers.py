# -*- coding: utf-8 -*-
from django.db import models


class EventRegistrationManager(models.Manager):

    def create_attending_registration(self, event, user):
        attending = True
        number = event.users_attending()+1
        return self.create(event=event, user=user, attending=attending, number=number)

    def create_waiting_registration(self, event, user):
        attending = False
        number = event.users_waiting()+1
        return self.create(event=event, user=user, attending=attending, number=number)

    def update_lists(self, event):
        self.fix_list_numbering(event=event)
        self.move_waiting_to_attending(event=event)

    def fix_list_numbering(self, event):
        attending_regs = self.filter(event=event, attending=True).order_by('date')
        for n, reg in enumerate(attending_regs, start=1):
            reg.number = n
            reg.save()

        waiting_regs = self.filter(event=event, attending=False).order_by('date')
        for n, reg in enumerate(waiting_regs, start=1):
            reg.number = n
            reg.save()

    def move_waiting_to_attending(self, event):
        free_places = event.free_places()
        waiting_regs = self.filter(event=event, attending=False).order_by('date')[:free_places]
        for reg in waiting_regs:
            reg.set_attending_and_send_email()
        self.fix_list_numbering(event)


class RelatedEventRegistrationManager(models.Manager):

    def __init__(self, event):
        self.event = event

    def get_queryset(self):
        from .eventregistration import EventRegistration
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
