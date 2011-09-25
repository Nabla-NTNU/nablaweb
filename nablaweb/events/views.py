# -*- coding: utf-8 -*-


import datetime
from django.contrib import messages as django_messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext, loader
from django.views.generic import TemplateView
from nablaweb.content.views import ContentListView, ContentDetailView, ContentDeleteView
from nablaweb.events.models import Event

# Administrasjon

def _admin_mov(request, instance):
    user_list = request.POST.getlist('user')
    text = request.POST.get('text')
    try:
        place = int(text)
        for user in user_list:
            user = User.objects.get(username=user)
            if instance.is_registered(user):
                instance.move_user_to_place(user, place)
    except (ValueError, User.DoesNotExist): pass
_admin_mov.short = 'mov'
_admin_mov.info = 'Flytt til'


def _admin_add(request, instance):
    text = request.POST.get('text')
    try:
        user = User.objects.get(username=text)
        instance.register_user(user)
    except User.DoesNotExist: pass
_admin_add.short = 'add'
_admin_add.info = 'Legg til'


def _admin_del(request, instance):
    user_list = request.POST.getlist('user')
    for user in user_list:
        try:
            user = User.objects.get(username=user)
            instance.deregister_user(user)
        except User.DoesNotExist: pass
_admin_del.short = 'del'
_admin_del.info = 'Fjern'


def administer(request, pk,
               actions=(_admin_add, _admin_mov, _admin_del),
               view='event_admin'):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        action_name = request.POST.get('action')
        for action in actions:
            if action.short == action_name:
                action(request, event)
                break

        # Unngå at handlingen utføres på nytt dersom brukeren laster siden om igjen
        return HttpResponseRedirect(reverse(view, kwargs={'pk': pk}))

    registrations = event.eventregistration_set.all().order_by('number')
    return render_to_response('events/event_administer.html',
                              {'event': event,
                               'registrations': registrations,
                               'actions': [(a.short, a.info) for a in actions]},
                              context_instance=RequestContext(request))


class EventDeleteView(ContentDeleteView):
    model = Event


# Offentlig

class EventListView(ContentListView):
    model = Event


class EventDetailView(ContentDetailView):
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
    messages = {
        'noreg': 'Ingen registrering.',
        'closed': 'Påmeldingen har stengt.',
        'full': 'Arrangementet er fullt.',
        'attend': 'Du er påmeldt.',
        'queue': 'Du står på venteliste.',
        }
    event = get_object_or_404(Event, pk=event_id)
    token = event.register_user(request.user)
    message = messages[token]
    django_messages.add_message(request, django_messages.INFO, message)
    return HttpResponseRedirect(reverse('event_detail', kwargs={'pk': event_id}))


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
