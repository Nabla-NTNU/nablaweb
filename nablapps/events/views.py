"""
Views for events app
"""
import datetime
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.template import loader
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import get_user_model

from django.utils.safestring import mark_safe

from braces.views import (PermissionRequiredMixin,
                          LoginRequiredMixin,
                          StaticContextMixin,
                          MessageMixin)

from nablapps.core.view_mixins import AdminLinksMixin

from .models.event import Event, attending_events
from .models.eventregistration import EventRegistration
from .exceptions import (EventException, UserRegistrationException, EventFullException,
                         RegistrationNotAllowed, RegistrationNotOpen, RegistrationAlreadyExists,
                         RegistrationNotRequiredException, DeregistrationClosed)
from .event_calendar import EventCalendar
from .forms import RegisterAttendanceForm

from nablapps.accounts.models import NablaUser

User = get_user_model()


class AdministerRegistrationsView(StaticContextMixin,
                                  PermissionRequiredMixin,
                                  MessageMixin,
                                  DetailView):
    """Viser påmeldingslisten til et Event med mulighet for å melde folk på og av."""
    model = Event
    template_name = "events/event_administer.html"
    permission_required = 'events.administer'
    actions = {"add": ("Legg til", "register_user"),
               "del": ("Fjern", "deregister_users")}
    static_context = {'actions': [(key, name) for key, (name, _) in actions.items()]}

    def post(self, request, pk):
        """Handle http post request"""
        action_key = request.POST.get('action')
        _, method = self.actions[action_key]
        getattr(self, method)()
        return HttpResponseRedirect(reverse('event_admin', kwargs={'pk': pk}))

    def register_user(self):
        """Melder på brukeren nevnt i POST['text'] på arrangementet."""
        username = self.request.POST.get('text')

        #Tar inn verdien True fra checkboksen hvis den er markert
        if self.request.POST.get("Regelboks") == "True":
            regelbryting = True
        else:
            regelbryting = False

        if not username:
            self.messages.warning("Ingen brukernavn skrevet inn.")
            return
        try:
            user = User.objects.get(username=username)

            #Legger brukeren i listen.
            self.get_object().register_user(user, ignore_restrictions = regelbryting)
        except (User.DoesNotExist, UserRegistrationException) as ex:
            self.messages.warning(
                f"Kunne ikke legge til {username} i påmeldingslisten. "
                f"Returnert error var: {type(ex).__name__}: {str(ex)}. "
                "Ta kontakt med WebKom, og oppgi denne feilmeldingen "
                "dersom du tror dette er en feil.")

    def deregister_users(self):
        """Melder av brukerne nevnt i POST['user']."""
        user_list = self.request.POST.getlist('user')
        if not user_list:
            self.messages.warning("Ingen brukere krysset av!")

        for username in user_list:
            try:
                user = User.objects.get(username=username)
                self.get_object().deregister_user(user, respect_closed=False)
            except (User.DoesNotExist, UserRegistrationException) as ex:
                self.messages.warning(
                    f"Kunne ikke fjerne {username} fra påmeldingslisten. "
                    f"Returnert error var: {type(ex).__name__}: {str(ex)}. "
                    "Ta kontakt med WebKom, og oppgi denne feilmeldingen "
                    "dersom du tror dette er en feil.")

def calendar(request, year=None, month=None):
    """
    Renders a calendar with models from the chosen month
    """
    today = datetime.date.today()
    year = int(year) if year else today.year
    month = int(month) if month else today.month
    try:
        first_of_month = datetime.date(year, month, 1)
    except ValueError:  # Not a valid year and month
        raise Http404

    events = Event.objects.filter(
        event_start__year = year,
        event_start__month = month)
    cal = EventCalendar(events, year, month).formatmonth(year, month)

    user = request.user
    future_attending_events = attending_events(user, today)

    months = year*12 + month - 1 # months since epoch (Christ)
    month_list = [datetime.date(m//12, m%12+1, 1) for m in range(months-5, months+7)]

    # Get some random dates in the current, next, and previous month.
    # These dates are used load the calendar for that month.
    # * prev is some day in the previous month
    # * this is some day in this month
    # * next is some day in the next month
    context = {
        'calendar': mark_safe(cal),
        'prev': first_of_month - datetime.timedelta(27),
        'this': first_of_month,
        'next': first_of_month + datetime.timedelta(32),
        'future_attending_events': future_attending_events,
        'month_list': month_list
    }

    return render(request, 'events/event_list.html', context)


class EventRegistrationsView(PermissionRequiredMixin, DetailView):
    """Viser en liste over alle brukere påmeldt til arrangementet."""
    model = Event
    context_object_name = "event"
    template_name = "events/event_registrations.html"
    permission_required = 'events.add_event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        regs = event.eventregistration_set
        context['eventregistrations'] = regs.order_by('-attending', 'user__last_name')
        return context


class EventDetailView(AdminLinksMixin, MessageMixin, DetailView):
    """Viser arrangementet."""
    model = Event
    context_object_name = "event"
    template_name = 'events/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        user = self.request.user

        if user.is_authenticated:
            # Innlogget, så sjekk om de er påmeldt
            try:
                context['is_registered'] = event.is_registered(user)
                context['is_attending'] = event.is_attending(user)
                context['is_waiting'] = event.is_waiting(user)
            except EventException as e:
                self.messages.error(e)

        context['type'] = "bedpres" if event.is_bedpres else "event" # Used to include correct template
        return context

    def get_admin_links(self):
        if not self.object.registration_required:
            return super().get_admin_links()
        return [
            {
                "name": "Administrer påmeldinger",
                "glyphicon_symbol": "user",
                "url": reverse("event_admin", args=[self.object.id]),
            },
            {
                "name": "Påmeldingsliste",
                "glyphicon_symbol": "list",
                "url": reverse("event_registrations", args=[self.object.id]),
            },
            *super().get_admin_links()
        ]



class UserEventView(LoginRequiredMixin, TemplateView):
    """Show list of events the logged in user is registered to"""
    template_name = 'events/event_showuser.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        context_data['user'] = user
        if user.is_authenticated:
            regs = user.eventregistration_set.all().order_by('event__event_start')
            context_data['eventregistration_list'] = regs
            context_data['is_on_a_waiting_list'] = regs.filter(attending=False).exists()
            context_data['is_attending_an_event'] = regs.filter(attending=True).exists()
        return context_data


class RegisterUserView(LoginRequiredMixin,
                       MessageMixin,
                       DetailView):
    """View for at en bruker skal kunne melde seg av og på."""

    model = Event
    template_name = 'events/event_detail.html'

    def post(self, *args, **kwargs): # pylint: disable=W0613
        """Handle http post request"""
        reg_type = self.request.POST['registration_type']
        user = self.request.user

        if reg_type == "registration":
            message = self.register_user(user)
        elif reg_type == "deregistration":
            message = self.deregister_user(user)
        else:
            message = "Her skjedde det noe galt."

        self.messages.info(message)
        return HttpResponseRedirect(self.get_object().get_absolute_url())

    def register_user(self, user):
        """Prøver å melde en bruker på arrangementet.

        Returnerer en melding som er ment for brukeren.
        """
        try:
            reg = self.get_object().register_user(user)
        except EventFullException:
            return "Arrangementet er fullt"
        except RegistrationNotAllowed as e:
            # Include e to allow more precise reason for NotAllowed
            return 'Du har ikke lov til å melde deg på dette arrangementet. ' + str(e)
        except RegistrationNotOpen:
            return 'Påmeldingen er ikke åpen.'
        except RegistrationAlreadyExists:
            return "Du er allerede påmeldt."
        except RegistrationNotRequiredException:
            return "Arrangementet har ikke påmelding."
        return "Du er påmeldt" if reg.attending else "Du står nå på venteliste."

    def deregister_user(self, user):
        """Prøver å melde en bruker av arrangementet.

        Returnerer en melding som er ment for brukeren.
        """
        try:
            self.get_object().deregister_user(user)
        except DeregistrationClosed:
            return "Avmeldingsfristen er ute."
        return "Du er meldt av arrangementet."

class RegisterAttendanceView(DetailView):
    """Used by event admins to register attendance
    Usage:
     1. User is asked if penalties should be registered for the event.
        This creates penalties for all registered users.
     2. As users are registered, their penalties are deletd."""
    model = Event
    template_name = "events/register_attendance.html"


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        attending = EventRegistration.objects.filter(event=self.object, attending=True)
        redirection = redirect(self.request.resolver_match.view_name, kwargs.pop('pk', 1))

        # Give all attending penalty and return
        # if 'activate_penalties' in request.POST:
        #    attending.update(penalty=1)
        #    return redirection

        # # Register given list
        # user_penalty_list = []
        # for q in request.POST: # Generate list over users to get a penalty
        #     if q.startswith('user_penalty'):
        #         user_penalty_list.append(request.POST[q])
#        attending.update(penalty=0)
        # attending.filter(pk__in=user_penalty_list).update(penalty=True)

        for q in request.POST:
            if q.startswith('user_penalty_'):
                pk = q.split('_')[-1]
                penalty_value = request.POST[q]
                reg_req = attending.get(pk=pk)
                reg_req.penalty = penalty_value
                reg_req.save()

        # Register given card key
        attendance_form = RegisterAttendanceForm(request.POST)
        if not attendance_form.is_valid():
            context = self.get_context_data(**kwargs)
            context['form'] = attendance_form
            return render(request,self.template_name, context)
        card_key = attendance_form.cleaned_data['user_card_key']
        if card_key is not None:
            user = NablaUser.objects.get_from_rfid(card_key)
            reg = EventRegistration.objects.get(user=user, event=self.object)
            reg.penalty = 0
            reg.save()

        return redirection


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        registrations = event.eventregistration_set.filter(attending=True)
        context['registrations'] = registrations.order_by('user__first_name')
        context['form'] = RegisterAttendanceForm()

        # Penalty rules represents the different options for penalties
        # It is a dict with the following signature:
        # {rule_name(string): rule(dict)}, where rule is
        # {option_name(string), option_penalty_count(int)}

        penalty_rules = {'bedpres': {'Oppmøte': 0, 'Oppmøte for seint': 1, 'Ikke møtt opp': 2},
                         'arr_med_betaling' : {'Betalt': 0, 'Betalt etter purring': 1, 'Ikke betalt': 4},
                         'arr_uten_betaling': {'Møtt opp': 0, 'Ikke møtt opp': 1}}
        context['rules'] = list(penalty_rules.values())[2]
        return context


def ical_event(request, event_id):
    """Returns a given event or bedpres as an iCal .ics file"""

    event = Event.objects.get(id=event_id)

    # Use the same template for both Event and BedPres.
    template = loader.get_template('events/event_icalendar.ics')
    context = {'event_list': (event,), }
    response = HttpResponse(template.render(context), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=Nabla_%s.ics' % event.slug
    return response
