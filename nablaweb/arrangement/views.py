# -*- coding: utf-8 -*-

# arrangement/views.py

from nablaweb.arrangement.models import Event
from nablaweb.arrangement.forms import EventForm
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import datetime
import re
from collections import OrderedDict

# Administrasjon

def create_or_edit_event(request, event_id=None):
    if event_id is None:
        event = Event()
    else:
        event = get_object_or_404(Event, id=event_id)
    if request.method != 'POST':
        form = EventForm(instance=event,
                         initial={'registration_required': event.registration_deadline is not None},
                         )
    else:
        form = EventForm(data=request.POST,
                         instance=event,
                         initial={'registration_required': event.registration_deadline is not None},
                         )
        if form.is_valid():
            event = form.save(commit=False)
            if event_id is None:
                event.created_by = request.user
            else:
                event.last_changed_by = request.user
            event.test_event_fields()
            event.save()
            return HttpResponseRedirect(reverse('arrangement.views.show_event', args=(event.id,)))
    return render_to_response('arrangement/create_event.html', {'form': form}, context_instance=RequestContext(request))


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
    return render_to_response('arrangement/administer_event.html',
                              {'event': event, 'registrations': registrations, 'actions': actions, 'check_boxes': check_boxes},
                              context_instance=RequestContext(request))


def edit(request, event_id):
    return HttpResponse("Not implemented.")


def delete(request, event_id):
    return HttpResponse("Not implemented.")


# Offentlig

def list_events(request):
    return render_to_response('arrangement/list_events.html', {'content_list': Event.objects.all()})


def show_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render_to_response('arrangement/base_event.html', {'content': event})


# Bruker

def show_user(request):
    event_list = request.user.eventregistration_set.all()
    penalty_list = request.user.eventpenalty_set.all()
    return render_to_response('arrangement/showuser.html', {'event_list': event_list, 'penalty_list': penalty_list, 'member': request.user})


def register_user(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    message = event.register_user(request.user)
    return render_to_response('arrangement/base_event.html', {'content': event, 'messages': (message,)})


# Eksporter

def ical_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    template = loader.get_template('arrangement/icalendar.ics')
    context = Context({'event_list': (event,),})
    response = HttpResponse(template.render(context), mimetype='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=Nabla_%s.ics' % event.title.replace(' ', '_')
    return response


def ical_user(request):
    return HttpResponse("Not implemented.")
