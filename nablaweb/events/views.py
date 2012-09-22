# -*- coding: utf-8 -*-


import datetime
from django.contrib import messages as django_messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext, loader
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from nablaweb.news.views import NewsListView, NewsDetailView, NewsDeleteView
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


class EventDeleteView(NewsDeleteView):
    model = Event


# Offentlig

class EventListView(ListView):
    model = Event
    context_object_name = "event_list"
    queryset = Event.objects.all()

    # TODO: For performance reasons, only fetch the needed events.
    # That is, from Monday in the first week, to Sunday in the last week.

    def get_context_data(self, **kwargs):
        # Get the context from the superclass
        context = super(EventListView, self).get_context_data(**kwargs)
        
        # Penalties
        user = self.request.user
        if user.is_authenticated():
            context['penalty_list'] = user.eventpenalty_set.all()

        # Functions to be used
        from datetime import date, timedelta
        from calendar import monthrange

        today = date.today()

        # Set parameters from url. (/year/month)
        try:
            year = int(self.args[0])
        except IndexError:
            year = today.year

        try:
            month = int(self.args[1])
        except IndexError:
            month = today.month
        
        monthdays = monthrange(year, month)
        weeknodelta = date(year, month, monthdays[1]).isocalendar()[1] - date(year, month, 1).isocalendar()[1]
        
        # Weeks to be displayed
        if (weeknodelta == 5):
            weeks = 6
        else:
            weeks = 5

        # Get the monday at the start of the calendar
        first = date(year, month, 1)
        first_monday = first - timedelta(days=first.weekday())
        #  last_sunday = first + timedelta(weeks=weeks, days=6)

        # Object to add to context
        calendar = {'first': first, 'weeks': []}

        for week in range(0, weeks):
            # Add an empty week, with weeknumber
            calendar['weeks'].append({'days': []})
            for daynumber in range(0, 7):
                # Get the day
                day = first_monday + timedelta(days=week * 7 + daynumber)

                # If monday, get the weeknumber and add to current week
                if day.weekday() == 0:
                    calendar['weeks'][week]['weeknumber'] = day.isocalendar()[1]

                # Get the events which start at the current day,
                # or between two dates if an end date exists
                events = [event for event in context['event_list']
                        if (event.event_end and event.event_start.date() <= day
                        and day <= event.event_end.date()) or event.event_start.date() == day]

                # Add it to the week
                calendar['weeks'][week]['days'].append({
                    'date': day.day,
                    'events': events,
                    'differentmonth': (day.month != month),
                    'current': (day == today),
                })

        # Add next and previous
        calendar['prev'] = first_monday - timedelta(days=1)
        calendar['next'] = first + timedelta(days=31)

        # Add it to the request context
        context['calendar'] = calendar
        return context


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
            context_data['penalty_list'] = user.eventpenalty_set.all()
        return context_data

@login_required
def register_user(request, event_id):
    messages = {
        'noreg': 'Ingen registrering.',
        'closed': 'Påmeldingen har stengt.',
        'full': 'Arrangementet er fullt.',
        'attend': 'Du er påmeldt.',
        'queue': 'Du står på venteliste.',
        'reg_exists': 'Du er allerede påmeldt.',
        }
    event = get_object_or_404(Event, pk=event_id)
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
    token = event.deregister_user(request.user)
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
