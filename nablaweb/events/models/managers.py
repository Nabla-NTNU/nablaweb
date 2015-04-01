# -*- coding: utf-8 -*-
from django.db import models


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
