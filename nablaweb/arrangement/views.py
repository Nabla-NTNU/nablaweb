#!/usr/bin/env python
# -*- coding: utf-8 -*-

# arrangement/views.py

from nablaweb.arrangement.models import Event, NoShowDot
from nablaweb.arrangement.forms import EventForm
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.contrib.auth.models import User
import datetime

# Administrasjon

def create(request):
    # TODO: Lag en liste over arrangementtyper bruker kan opprette.
    user_types = Event.event_types()
    user_choices = Event.event_choices()
    event_type = request.POST.get('event_type')
    form = EventForm(request.POST)
    if request.method != 'POST' \
            or event_type not in user_types:
        response = render_to_response('arrangement/chooseeventtype.html', RequestContext(request, {'event_choices': user_choices}))
    elif form.is_valid():
        print "New event:"
        cd = form.cleaned_data
        for k, v in cd.iteritems():
            print "%-25s %s" % (k, v)
        # TODO: Stygg hack som bør fikses
        del cd['allow_deregistration']
        del cd['has_registration_deadline']
        event = Event(**form.cleaned_data)
        event.save()
        # TODO: Kan save() feile?
        response = HttpResponseRedirect('/arrangement/%d/' % event.id)
    else:
        print form.errors
        if request.POST.get('init'):
            form = EventForm(
                initial={'event_type': event_type,
                         'event_start': datetime.datetime.now(),},
                )
        response = render_to_response('arrangement/create_event.html', RequestContext(request, {'form': form, 'event_type': event_type, 'options': Event.event_options(event_type)}))
    return response

def status(request, event_id):
    return HttpResponse("Not implemented.")

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
    dot_list = request.user.noshowdot_set.all()
    return render_to_response('arrangement/showuser.html', {'event_list': event_list, 'dot_list': dot_list, 'member': request.user})

def registration(request, event_id):
    return HttpResponse("Not implemented.")

def register(request, event_id):
    return HttpResponse("Not implemented.")


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
