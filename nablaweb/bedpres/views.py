# -*- coding: utf-8 -*-

from django.views.generic import FormView

from events.views import EventDetailView, RegisterUserView
from .forms import BPCForm
from .models import BedPres

# Administrasjon

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


class BedPresRegisterUserView(RegisterUserView):
    model = BedPres

    def register_user(self, bedpres, user):
        return bedpres.register_user(user)

    def deregister_user(self, bedpres, user):
        return bedpres.deregister_user(user)


class BedPresDetailView(EventDetailView):
    model = BedPres
    context_object_name = "bedpres"
