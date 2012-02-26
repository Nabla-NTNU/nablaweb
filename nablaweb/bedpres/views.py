# -*- coding: utf-8 -*-


# Ical event til administer er kun lagt til for å fjerne en error som dukket opp hos meg. (Missing view)
from nablaweb.events.views import EventListView, EventDetailView, EventDeleteView, UserEventView, ical_event, register_user, administer
from nablaweb.bedpres.forms import BPCForm
from nablaweb.bedpres.models import BedPres
from django.views.generic import FormView, ListView
import bpc_core


# Administrasjon

class BedPresDeleteView(EventDeleteView):
    model = BedPres


class BPCFormView(FormView):
    template_name = 'bedpres/bedpres_bpc_menu.html'
    form_class = BPCForm
    # TODO: Finn et bedre sted å videresende til.
    success_url = '/'

    def form_valid(self, form):
        events_to_create = form.cleaned_data['events']
        print dir(self)
        for event in form.available_events:
            if event['id'] in events_to_create:
                # TODO: Sjekk hvorfor DateTimeField håndterer datostrengen fra BPC.
                # TODO: Fiks bilde.
                bedpres = BedPres(
                    bpcid = event['id'],
                    headline = event['title'],
#                    picture = event['logo'],
                    description = event['description'],
                    organizer = event['title'],
                    location = event['place'],
                    event_start = event['time'],
                    registration_required = True,
                    registration_deadline = event['deadline'],
                    registration_start = event['registration_start'],
                    places = event['seats'],
                    has_queue = bool(int(event['waitlist_enabled'])),
                    )
                bedpres.created_by = self.request.user
                bedpres.last_changed_by = self.request.user
                bedpres.save()
        return super(BPCFormView, self).form_valid(form)


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
