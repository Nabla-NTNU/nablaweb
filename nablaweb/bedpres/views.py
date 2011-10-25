# -*- coding: utf-8 -*-


# Ical event til administer er kun lagt til for å fjerne en error som dukket opp hos meg. (Missing view)
from nablaweb.events.views import EventListView, EventDetailView, EventDeleteView, UserEventView, ical_event, register_user, administer
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
