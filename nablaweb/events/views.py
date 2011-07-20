# -*- coding: utf-8 -*-


import datetime
import re
from collections import OrderedDict
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from nablaweb.content.views import ContentUpdateView
from nablaweb.events.models import Event
from nablaweb.events.forms import EventForm


# Administrasjon

class EventUpdateView(ContentUpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    form_base = 'events/event_form_base.html'
    success_detail = 'event_detail'

    def get_initial(self):
        initial = super(EventUpdateView, self).get_initial()
        initial['registration_required'] = self.object.registration_deadline is not None
        return initial


def administer(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    registrations = event.eventregistration_set.all().order_by('number')
    actions = OrderedDict([('mov','Flytt til'), ('del','Fjern'), ('add','Legg til'), ('mrk','Merk alle')])
    check_boxes = False

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
        elif action == 'mrk':
            check_boxes = True

    # TODO: Endre til HttpResponseRedirect eller triks med POST/GET,
    # for å unngå at samme handling utføres flere ganger når brukeren
    # laster siden på nytt.
    return render_to_response('events/event_administer.html',
                              {'event': event, 'registrations': registrations, 'actions': actions, 'check_boxes': check_boxes},
                              context_instance=RequestContext(request))


def edit(request, event_id):
    return HttpResponse("Not implemented.")


def delete(request, event_id):
    return HttpResponse("Not implemented.")


# Offentlig


# Bruker

def show_user(request):
    event_list = request.user.eventregistration_set.all()
    penalty_list = request.user.eventpenalty_set.all()
    return render_to_response('events/event_showuser.html', {'event_list': event_list, 'penalty_list': penalty_list, 'member': request.user})


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
