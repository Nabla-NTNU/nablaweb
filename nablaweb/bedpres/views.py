# -*- coding: utf-8 -*-

from django.views.generic import FormView, DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import  get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages as django_messages

import bpc_core
from bpc_core import BPCResponseException
from events.views import RegisterUserView as EventRegisterUserView

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


class RegisterUserView(EventRegisterUserView):
    model = BedPres

    def register_user(self, bedpres, user):
        return bedpres.register_user(user)

    def deregister_user(self, bedpres, user):
        return bedpres.deregister_user(user)


class BedPresDetailView(DetailView):
    model = BedPres
    context_object_name = "bedpres"

    def get_context_data(self, **kwargs):
        context = super(BedPresDetailView, self).get_context_data(**kwargs)
        object_name = self.object.content_type.model
        event = self.object
        user = self.request.user

        if user.is_anonymous():
            context['is_registered'] = False
            context['is_attending'] = False
        else:
            # Innlogget, så sjekk om de er påmeldt
            context['is_registered'] = event.is_registered(user)
            context['is_attending'] = event.is_attending(user)
        return context

