# -*- coding: utf-8 -*-

from content.views import EventDetailView, RegisterUserView
from .event_overrides import *
from .utils import InvalidCardNum
from .bpcmixin import WrongClass


class BedPresRegisterUserView(RegisterUserView):
    model = BedPres

    def register_user(self, user):
        try:
            super().register_user(user)
        except InvalidCardNum:
            return "Du ble ikke påmeldt fordi du mangler gyldig NTNU-kortnummer."
        except WrongClass as e:
            if e.user.get_class_number() == 0:
                return (
                    "Du ble ikke påmeldt fordi du ikke er registrert på noe kull. "
                    "Send en epost til webkom@nabla.ntnu.no for å fikse det.")
            else:
                return (
                    "Du ble ikke påmeldt fordi du går i feil klasse for dette arrangementet.\n"
                    "I følge våre systemer går du i {klasse}. klasse og arrangementet "
                    "er kun åpent for {event.bpc_event.min_year}. til {event.bpc_event.max_year}. klasse."
                ).format(klasse=e.user.get_class_number(), event=e.event)


class BedPresDetailView(EventDetailView):
    model = BedPres
    template_name = 'bedpres/bedpres_detail.html'
    context_object_name = "bedpres"
