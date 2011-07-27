# -*- coding: utf-8 -*-


import datetime
import re
from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext, loader
from django.views.generic import TemplateView
from nablaweb.content.views import SiteContentListView, SiteContentDetailView, SiteContentDeleteView
from nablaweb.events.forms import EventForm
from nablaweb.events.models import Event


# Administrasjon

def administer(request, pk):
    event = get_object_or_404(Event, pk=pk)
    actions = OrderedDict([('mov','Flytt til'),
                           ('del','Fjern'),
                           ('add','Legg til'),])

    if request.method == 'POST':
        action = request.POST.get('action')
        user_list = request.POST.getlist('user')
        text = request.POST.get('text')
        if action == 'mov':
            try:
                place = int(text)
                for user in user_list:
                    user = User.objects.get(username=user)
                    if event.is_registered(user):
                        event.move_user_to_place(user, place)
            except (ValueError, User.DoesNotExist): pass
        elif action == 'del':
            for user in user_list:
                try:
                    user = User.objects.get(username=user)
                    event.deregister_user(user)
                except User.DoesNotExist: pass
        elif action == 'add':
            try:
                user = User.objects.get(username=text)
                event.register_user(user)
            except User.DoesNotExist: pass

        # Unngå at handlingen utføres på nytt dersom brukeren laster siden om igjen
        return HttpResponseRedirect(reverse('event_admin', kwargs={'pk': pk}))

    registrations = event.eventregistration_set.all().order_by('number')
    return render_to_response('events/event_administer.html',
                              {'event': event, 'registrations': registrations, 'actions': actions, 'method': 'GET'},
                              context_instance=RequestContext(request))


class EventDeleteView(SiteContentDeleteView):
    model = Event


# Offentlig

class EventListView(SiteContentListView):
    model = Event


class EventDetailView(SiteContentDetailView):
    model = Event


# Bruker

class UserEventView(TemplateView):
    template_name = 'events/event_showuser.html'

    def get_context_data(self, **kwargs):
        context_data = super(UserEventView, self).get_context_data(**kwargs)
        user = self.request.user
        context_data['user'] = user
        context_data['eventregistration_list'] = user.eventregistration_set.all().order_by('event__event_start')
        context_data['penalty_list'] = user.eventpenalty_set.all()
        return context_data


def register_user(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    message = event.register_user(request.user)
    return render_to_response('events/event_detail.html', {'content': event, 'messages': (message,)})


# Eksporter

def ical_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    template = loader.get_template('events/event_icalendar.ics')
    context = Context({'event_list': (event,),})
    response = HttpResponse(template.render(context), mimetype='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=Nabla_%s.ics' % event.title.replace(' ', '_')
    return response


def ical_user(request):
    return HttpResponse("Not implemented.")
