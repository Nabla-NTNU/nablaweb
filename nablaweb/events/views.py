# -*- coding: utf-8 -*-


from django.contrib import messages as django_messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import Context, RequestContext, loader
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model; User = get_user_model()
from django.utils.safestring import mark_safe

import datetime
from itertools import chain
from braces.views import PermissionRequiredMixin, LoginRequiredMixin

from bedpres.models import BedPres
from .models import Event, EventRegistration
from .event_calendar import EventCalendar


class AdministerRegistrationsView(PermissionRequiredMixin, DetailView):
    """Viser påmeldingslisten til et Event med mulighet for å melde folk på og av."""
    model = Event
    template_name = "events/event_administer.html"
    permission_required = 'events.administer'

    def __init__(self, **kwargs):
        super(AdministerRegistrationsView, self).__init__(**kwargs)
        self.actions = (self.register_user, self.deregister_users)

    def get_context_data(self, **kwargs):
        context = super(AdministerRegistrationsView, self).get_context_data(**kwargs)
        context['actions'] = [(a.short, a.info) for a in self.actions]
        return context

    def post(self, *args, **kwargs):
        self.event = self.get_object()
        action_name = self.request.POST.get('action')
        for action in self.actions:
            if action.short == action_name:
                action()
                break
        return HttpResponseRedirect(reverse('event_admin', kwargs={'pk': self.event.pk}))

    def register_user(self):
        """Melder på brukeren nevnt i POST['text'] på arrangementet."""
        username = self.request.POST.get('text')
        try:
            user = User.objects.get(username=username)
            self.event.register_user(user, ignore_restrictions=True)
        except User.DoesNotExist: pass
    register_user.short = 'add'
    register_user.info = 'Legg til'

    def deregister_users(self):
        """Melder av brukerne nevnt i POST['user']."""
        user_list = self.request.POST.getlist('user')
        for username in user_list:
            try:
                user = User.objects.get(username=username)
                self.event.deregister_user(user)
            except User.DoesNotExist: pass
    deregister_users.short = 'del'
    deregister_users.info = 'Fjern'



# Offentlig

def calendar(request, year=None, month=None):
    """
    Renders a calendar with events from the chosen month
    """
    today = datetime.date.today()
    year = int(year) if year else today.year
    month = int(month) if month else today.month

    # Get this months events and bedpreser separately
    events = Event.objects.select_related("content_type").filter(
            event_start__year=year, event_start__month=month)
    bedpress = BedPres.objects.select_related("content_type").filter(
            event_start__year=year, event_start__month=month)

    # Combine them to a single calendar
    try:
        cal = EventCalendar(chain(events, bedpress)).formatmonth(year, month)
    except ValueError:
        raise Http404

    if request.user.is_authenticated():
        future_attending_events = request.user.eventregistration_set.filter(event__event_start__gte=today)
    else:
        future_attending_events = []

    # Get some random dates in the current, next, and previous month.
    # These dates are used load the calendar for that month.
    # * prev is some day in the previous month
    # * this is some day in this month
    # * next is some day in the next month
    return render(request, 'events/event_list.html', {
        'calendar': mark_safe(cal),
        'prev': datetime.date(year, month, 1) - datetime.timedelta(27),
        'this': datetime.date(year, month, 1),
        'next': datetime.date(year, month, 1) + datetime.timedelta(32),
        'future_attending_events': future_attending_events,
    })


class EventRegistrationsView(PermissionRequiredMixin, DetailView):
    model = Event
    context_object_name = "event"
    template_name = "events/event_registrations.html"
    permission_required = 'events.add_event'

    def get_context_data(self, **kwargs):
        context = super(EventRegistrationsView, self).get_context_data(**kwargs)
        event = self.object
        context['eventregistrations'] = event.eventregistration_set.order_by('-attending','user__last_name')
        object_name = self.object.content_type.model
        return context


class EventDetailView(DetailView):
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

class UserEventView(LoginRequiredMixin, TemplateView):
    template_name = 'events/event_showuser.html'

    def get_context_data(self, **kwargs):
        context_data = super(UserEventView, self).get_context_data(**kwargs)
        user = self.request.user
        context_data['user'] = user
        if user.is_authenticated():
            regs = user.eventregistration_set.all().order_by('event__event_start')
            context_data['eventregistration_list'] = regs
            context_data['is_on_a_waiting_list']  = regs.filter(attending=False).exists()
            context_data['is_attending_an_event'] = regs.filter(attending=True).exists()
        return context_data


class RegisterUserView(LoginRequiredMixin, DetailView):
    """View for at en bruker skal kunne melde seg av og på."""

    model = Event
    error_messages = {
        # Registration messages
        'noreg'     : 'Ingen registrering.',
        'unopened'  : 'Påmeldingen har ikke åpnet.',
        'closed'    : 'Påmeldingen har stengt.',
        'full'      : 'Arrangementet er fullt.',
        'reg_exists': 'Du er allerede påmeldt.',
        'not_allowed' : 'Du har ikke lov til å melde deg på dette arrangementet.',
        # Deregistration messages 
        'not_reg': 'Du verken var eller er påmeldt.',
        'dereg_closed': 'Fristen for å melde seg av er gått ut.',
        'not_allowed': 'Ta kontakt med ArrKom for å melde deg av.',
        }

    def post(self, *args, **kwargs):
        reg_type = self.request.POST['registration_type']
        event = self.get_object()
        user = self.request.user

        if reg_type == "registration":
            message = self.register_user(event, user)
        elif reg_type == "deregistration":
            message = self.deregister_user(event, user)
        else:
            message = "Her skjedde det noe galt."

        django_messages.add_message(self.request, django_messages.INFO, message)
        return HttpResponseRedirect(event.get_absolute_url())

    def register_user(self, event, user):
        """Prøver å melde en bruker på arrangementet.

        Returnerer en melding som ment for brukeren.
        """
        try:
            reg = event.register_user(user)
        except RegistrationException as e:
            return self.error_messages[e.token]
        else:
            if reg.attending:
                return "Du er påmeldt"
            else:
                return "Du står nå på venteliste."

    def deregister_user(self, event, user):
        """Prøver å melde en bruker av arrangementet.

        Returnerer en melding som ment for brukeren.
        """
        try:
            event.deregister_user(user)
        except RegistrationException as e:
            return self.error_messages[e.token]
        else:
            return "Du er meldt av arrangementet."


def ical_event(request, event_id):
    """Returns a given event or bedpres as an iCal .ics file"""

    # Try Event first, then BedPres. 404 if none of them are found.
    try:
        event = Event.objects.get(pk=event_id)
    except:
        event = get_object_or_404(BedPres, pk=event_id)

    # Use the same template for both Event and BedPres.
    template = loader.get_template('events/event_icalendar.ics')
    context = Context({'event_list': (event,),})
    response = HttpResponse(template.render(context), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=Nabla_%s.ics' % event.slug
    return response
