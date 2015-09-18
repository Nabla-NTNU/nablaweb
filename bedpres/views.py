# -*- coding: utf-8 -*-

from content.views import EventDetailView, RegisterUserView
from .event_overrides import *
from .utils import InvalidCardNum


class BedPresRegisterUserView(RegisterUserView):
    model = BedPres

    def register_user(self, user):
        try:
            super().register_user(user)
        except InvalidCardNum:
            return "Du ble ikke påmeldt fordi du mangler gyldig NTNU-kortnummer."


class BedPresDetailView(EventDetailView):
    model = BedPres
    template_name = 'bedpres/bedpres_detail.html'
    context_object_name = "bedpres"
