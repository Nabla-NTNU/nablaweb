# -*- coding: utf-8 -*-


# Ical event til administer er kun lagt til for å fjerne en error som dukket opp hos meg. (Missing view)
from nablaweb.events.views import EventListView, EventDetailView, EventDeleteView, UserEventView, ical_event, register_user, administer
from nablaweb.bedpres.forms import BPCForm
from nablaweb.bedpres.models import BedPres
from django.views.generic import FormView, ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import  get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages as django_messages
import bpc_core
from bpc_core import BPCResponseException


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
        for event in form.available_events:
            if event['id'] in events_to_create:
                # TODO: Sjekk hvorfor DateTimeField håndterer datostrengen fra BPC.
                # TODO: Fiks bilde.
                bedpres = BedPres(
                    bpcid = event['id'],
                    headline = event['title'],
#                    picture = event['logo'],
                    body = event['description'],
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
oystein = BPCResponseException
from django.http import HttpResponse
@login_required
def register_user_view(request, bedpres_id):
    messages = {
        'noreg': 'Ingen registrering.',
        'closed': 'Påmeldingen har stengt.',
        'full': 'Arrangementet er fullt.',
        'attend': 'Du er påmeldt.',
        'queue': 'Du står på venteliste.',
        'reg_exists': 'Du er allerede påmeldt.',
        }
    event = get_object_or_404(BedPres, pk=bedpres_id)
    message  = event.register_user(request.user)
       
#    message = messages[token]
    django_messages.add_message(request, django_messages.INFO, message)
    return HttpResponseRedirect(event.get_absolute_url())

class BedPresListView(EventListView):
    model = BedPres
    context_object_name = "bedpres_list"


class BedPresDetailView(EventDetailView):
    model = BedPres
    context_object_name = "bedpres"


# Bruker

class UserBedPresView(UserEventView):
    template_name = 'events/event_showuser.html'
