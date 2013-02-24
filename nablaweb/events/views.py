# -*- coding: utf-8 -*-


import datetime
from django.contrib import messages as django_messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import Context, RequestContext, loader
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from nablaweb.news.views import NewsListView, NewsDetailView, NewsDeleteView
from nablaweb.events.models import Event, EventRegistration
from nablaweb.bedpres.models import BedPres
from itertools import chain
from events.event_calendar import EventCalendar

# Administrasjon

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
               actions=(_admin_add, _admin_del),
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


class EventDeleteView(NewsDeleteView):
    model = Event


# Offentlig

def calendar(request, year=None, month=None):
    """
    Renders a calendar with events from the chosen month
    """
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    events = Event.objects.select_related('content_type').order_by('event_start').filter(
        event_start__year=year, event_start__month=month
    )
    cal = EventCalendar(events).formatmonth(year, month)

    # prev is some day in the previous month
    # this is some day in this month
    # next is some day in the next month
    return render(request, 'events/event_list.html', {
        'calendar': mark_safe(cal),
        'prev': datetime.date(year, month, 1) - datetime.timedelta(27),
        'this': datetime.date(year, month, 1),
        'next': datetime.date(year, month, 1) + datetime.timedelta(32),
    })


class EventListView(ListView):
    model = Event
    context_object_name = "event_list"
    queryset = Event.objects.all() 


class EventDetailView(NewsDetailView):
    model = Event
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        object_name = self.object.content_type.model
        event = self.object
        user = self.request.user

        if user.is_anonymous():
            context['is_registered'] = False
        else:
            # Innlogget, så sjekk om de er påmeldt
            context['is_registered'] = event.is_registered(user)
            context['is_attending'] = event.is_attending(user)
            if context['is_registered']:
                # Henter eventregistration for denne brukeren hvis han/hun er påmeldt
                context['eventregistration'] = event.eventregistration_set.get(user=user)
        return context


# Bruker

class UserEventView(TemplateView):
    template_name = 'events/event_showuser.html'

    def get_context_data(self, **kwargs):
        context_data = super(UserEventView, self).get_context_data(**kwargs)
        user = self.request.user
        context_data['user'] = user
        if user.is_authenticated():
            context_data['eventregistration_list'] = user.eventregistration_set.all().order_by('event__event_start') 
            context_data['is_on_a_waiting_list'] = bool( filter(EventRegistration.is_waiting_place , context_data['eventregistration_list']) )
            context_data['penalty_list'] = user.eventpenalty_set.all()
        return context_data

@login_required
def register_user(request, event_id):
    messages = {
        'noreg'     : 'Ingen registrering.',
        'unopened'  : 'Påmeldingen har ikke åpnet.',
        'closed'    : 'Påmeldingen har stengt.',
        'full'      : 'Arrangementet er fullt.',
        'attend'    : 'Du er påmeldt.',
        'queue'     : 'Du står på venteliste.',
        'reg_exists': 'Du er allerede påmeldt.',
        'not_allowed' : 'Du har ikke lov til å melde deg på dette arrangementet.',
        }
    event = get_object_or_404(Event, pk=event_id)
    
    if event.registration_start and event.registration_start > datetime.datetime.now():
        token = 'unopened'
    elif event.registration_deadline and event.registration_deadline < datetime.datetime.now():
        token = 'closed'
    elif not event.allowed_to_attend(request.user):
        token = 'not_allowed'
    else:
        token = event.register_user(request.user)

    message = messages[token]
    django_messages.add_message(request, django_messages.INFO, message)
    return HttpResponseRedirect(event.get_absolute_url())

@login_required
def deregister_user(request, event_id):
    messages = {
        'not_reg': 'Du verken var eller er påmeldt.',
        'dereg_closed': 'Fristen for å melde seg av er gått ut.',
        'not_allowed': 'Ta kontakt med ArrKom for å melde deg av.',
        'dereg': 'Du er meldt av arrangementet.',
        }
    event = get_object_or_404(Event, pk=event_id)
    
    if event.deregistration_closed is None:
        token = 'not_allowed'
    elif  event.deregistration_closed():
        token = 'dereg_closed'
    else:
        token = event.deregister_user(request.user)

    message = messages[token]
    django_messages.add_message(request, django_messages.INFO, message)
    return HttpResponseRedirect(event.get_absolute_url())


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
