# -*- coding: utf-8 -*-

from events.views import EventDetailView, RegisterUserView
from .models import BedPres


class BedPresRegisterUserView(RegisterUserView):
    model = BedPres

    def register_user(self, bedpres, user):
        return bedpres.register_user(user)

    def deregister_user(self, bedpres, user):
        return bedpres.deregister_user(user)


class BedPresDetailView(EventDetailView):
    model = BedPres
    context_object_name = "bedpres"
