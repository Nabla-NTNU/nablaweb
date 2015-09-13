# -*- coding: utf-8 -*-


from django.contrib import messages as django_messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import Context, loader
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import get_user_model

User = get_user_model()
from django.utils.safestring import mark_safe

import datetime
from itertools import chain
from braces.views import (PermissionRequiredMixin,
                          LoginRequiredMixin,
                          StaticContextMixin)

from ..models.events import Event
from ..exceptions import *
from ..event_calendar import EventCalendar
from .mixins import AdminLinksMixin


class AdministerRegistrationsView(StaticContextMixin,
                                  PermissionRequiredMixin,
                                  DetailView):
    """Viser påmeldingslisten til et Event med mulighet for å melde folk på og av."""
    model = Event
    template_name = "events/event_administer.html"
    permission_required = 'events.administer'
    actions = {"add": ("Legg til", "register_user"),
               "del": ("Fjern", "deregister_users")}
    static_context = {'actions': [(key, name) for key, (name, _) in actions.items()]}

    def post(self, request, pk):
        action_key = request.POST.get('action')
        name, method = self.actions[action_key]
        getattr(self, method)()
        return HttpResponseRedirect(reverse('event_admin', kwargs={'pk': pk}))

    def register_user(self):
        """Melder på brukeren nevnt i POST['text'] på arrangementet."""
        username = self.request.POST.get('text')
        try:
            user = User.objects.get(username=username)
            self.get_object().add_to_attending_or_waiting_list(user)
        except (User.DoesNotExist, UserRegistrationException):
            pass

    def deregister_users(self):
        """Melder av brukerne nevnt i POST['user']."""
        user_list = self.request.POST.getlist('user')
        for username in user_list:
            try:
                user = User.objects.get(username=username)
                self.get_object().deregister_user(user)
            except (User.DoesNotExist, UserRegistrationException):
                pass


def get_current_events(year, month):
    # Get this months events and bedpreser separately
    events = Event.objects.select_related("content_type").filter(
        event_start__year=year,
        event_start__month=month)
    # bedpress = BedPres.objects.select_related("content_type").filter(
    #    event_start__year=year,
    #    event_start__month=month)

    # Combine them to a single calendar
    return events

CURRENT_EVENTS = None


def set_current_events(fun, override=False):
    global CURRENT_EVENTS
    if not CURRENT_EVENTS or override:
        CURRENT_EVENTS = fun


set_current_events(get_current_events)


def calendar(request, year=None, month=None):
    """
    Renders a calendar with events from the chosen month
    """
    today = datetime.date.today()
    year = int(year) if year else today.year
    month = int(month) if month else today.month
    try:
        first_of_month = datetime.date(year, month, 1)
    except ValueError:  # Not a valid year and month
        raise Http404

    events = CURRENT_EVENTS(year, month)
    cal = EventCalendar(chain(events)).formatmonth(year, month)

    user = request.user
    future_attending_events = user.eventregistration_set.filter(event__event_start__gte=today) \
        if user.is_authenticated() else []

    # Get some random dates in the current, next, and previous month.
    # These dates are used load the calendar for that month.
    # * prev is some day in the previous month
    # * this is some day in this month
    # * next is some day in the next month
    return render(request, 'events/event_list.html', {
        'calendar': mark_safe(cal),
        'prev': first_of_month - datetime.timedelta(27),
        'this': first_of_month,
        'next': first_of_month + datetime.timedelta(32),
        'future_attending_events': future_attending_events,
    })


class EventRegistrationsView(PermissionRequiredMixin, DetailView):
    """Viser en liste over alle brukere påmeldt til arrangementet."""
    model = Event
    context_object_name = "event"
    template_name = "events/event_registrations.html"
    permission_required = 'events.add_event'

    def get_context_data(self, **kwargs):
        context = super(EventRegistrationsView, self).get_context_data(**kwargs)
        event = self.object
        context['eventregistrations'] = event.eventregistration_set.order_by('-attending', 'user__last_name')
        return context


class EventDetailView(AdminLinksMixin, DetailView):
    """Viser arrangementet."""
    model = Event
    context_object_name = "event"
    template_name = 'events/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        event = self.object
        user = self.request.user

        if user.is_authenticated():
            # Innlogget, så sjekk om de er påmeldt
            context['is_registered'] = event.is_registered(user)
            context['is_attending'] = event.is_attending(user)
            context['is_waiting'] = event.is_waiting(user)
        return context


class UserEventView(LoginRequiredMixin, TemplateView):
    template_name = 'events/event_showuser.html'

    def get_context_data(self, **kwargs):
        context_data = super(UserEventView, self).get_context_data(**kwargs)
        user = self.request.user
        context_data['user'] = user
        if user.is_authenticated():
            regs = user.eventregistration_set.all().order_by('event__event_start')
            context_data['eventregistration_list'] = regs
            context_data['is_on_a_waiting_list'] = regs.filter(attending=False).exists()
            context_data['is_attending_an_event'] = regs.filter(attending=True).exists()
        return context_data


class RegisterUserView(LoginRequiredMixin, DetailView):
    """View for at en bruker skal kunne melde seg av og på."""

    model = Event

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
        except EventFullException:
            return "Arrangementet er fullt"
        except RegistrationNotAllowed:
            return 'Du har ikke lov til å melde deg på dette arrangementet.'
        except RegistrationNotOpen:
            return 'Påmeldingen er ikke åpen.'
        except RegistrationAlreadyExists:
            return "Du er allerede påmeldt."
        except RegistrationNotRequiredException:
            return "Arrangementet har ikke påmelding."
        return "Du er påmeldt" if reg.attending else "Du står nå på venteliste."

    def deregister_user(self, event, user):
        """Prøver å melde en bruker av arrangementet.

        Returnerer en melding som ment for brukeren.
        """
        try:
            event.deregister_user(user)
        except DeregistrationClosed:
            return "Avmeldingsfristen er ute."
        else:
            return "Du er meldt av arrangementet."


def ical_event(request, event_id):
    """Returns a given event or bedpres as an iCal .ics file"""

    # Try Event first, then BedPres. 404 if none of them are found.
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExcist:
        # event = get_object_or_404(BedPres, pk=event_id)
        event = None

    # Use the same template for both Event and BedPres.
    template = loader.get_template('events/event_icalendar.ics')
    context = Context({'event_list': (event,), })
    response = HttpResponse(template.render(context), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=Nabla_%s.ics' % event.slug
    return response
