# -*- coding: utf-8 -*-


# Ical event til administer er kun lagt til for å fjerne en error som dukket opp hos meg. (Missing view)
from nablaweb.events.views import EventListView, EventDetailView, EventDeleteView, UserEventView, ical_event, register_user, administer
from nablaweb.bedpres.models import BedPres
from django.views.generic import ListView
import bpc_core

# Administrasjon
class BedPresDeleteView(EventDeleteView):
    model = BedPres

class BedPresSelectFromBPC(ListView):
    context_object_name = "bedpres_list"
    template_name = 'bedpres/bedpres_bpc_menu.html'

    def get_queryset(self):
        return bpc_core.get_future_events()
    

# Offentlig

class BedPresListView(EventListView):
    model = BedPres
    context_object_name = "bedpres_list"


class BedPresDetailView(EventDetailView):
    model = BedPres
    context_object_name = "bedpres"

# Bruker

class UserBedPresView(UserEventView):
    template_name = 'events/event_showuser.html'
