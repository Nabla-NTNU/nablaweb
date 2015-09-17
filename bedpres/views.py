# -*- coding: utf-8 -*-

from content.views import EventDetailView, RegisterUserView
from bedpres.event_overrides import *


class BedPresRegisterUserView(RegisterUserView):
    model = BedPres

    def register_user(self, user):
        return self.get_object().register_user(user)

    def deregister_user(self, user):
        return self.get_object().deregister_user(user)


class BedPresDetailView(EventDetailView):
    model = BedPres
    template_name = 'bedpres/bedpres_detail.html'
    context_object_name = "bedpres"
