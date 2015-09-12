# -*- coding: utf-8 -*-

from content.views import EventDetailView, RegisterUserView
from bedpres.event_overrides import *


class BedPresRegisterUserView(RegisterUserView):
    model = BedPres


class BedPresDetailView(EventDetailView):
    model = BedPres
    template_name = 'bedpres/bedpres_detail.html'
    context_object_name = "bedpres"
