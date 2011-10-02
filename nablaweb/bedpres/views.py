# -*- coding: utf-8 -*-


from nablaweb.events.views import EventListView, EventDetailView, EventDeleteView, UserEventView
from nablaweb.bedpres.models import BedPres


# Administrasjon
class BedPresDeleteView(EventDeleteView):
    model = BedPres


# Offentlig

class BedPresListView(EventListView):
    model = BedPres


class BedPresDetailView(EventDetailView):
    model = BedPres


# Bruker

class UserBedPresView(UserEventView):
    template_name = 'events/event_showuser.html'
