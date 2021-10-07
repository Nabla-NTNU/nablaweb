"""
Views for events app
"""
import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView, TemplateView

from braces.views import (
    LoginRequiredMixin,
    MessageMixin,
    PermissionRequiredMixin,
    StaticContextMixin,
)

from nablapps.accounts.models import NablaUser
from nablapps.core.view_mixins import AdminLinksMixin

from .event_calendar import EventCalendar
from .exceptions import (
    DeregistrationClosed,
    EventException,
    EventFullException,
    EventNotStartedException,
    RegistrationAlreadyExists,
    RegistrationNotAllowed,
    RegistrationNotOpen,
    RegistrationNotRequiredException,
    UserAlreadyRegistered,
    UserAttendanceException,
    UserNotAttending,
    UserRegistrationException,
)
from .forms import FilterEventsForm  # Used in EventMainPage
from .models.event import Event, attending_events
from .models.eventregistration import EventRegistration

User = get_user_model()


class AdministerRegistrationsView(
    StaticContextMixin, PermissionRequiredMixin, MessageMixin, DetailView
):
    """Viser påmeldingslisten til et Event med mulighet for å melde folk på og av."""

    model = Event
    template_name = "events/event_administer.html"
    permission_required = "events.administer"
    actions = {
        "add": ("Legg til", "register_user"),
        "del": ("Fjern", "deregister_users"),
    }
    static_context = {"actions": [(key, name) for key, (name, _) in actions.items()]}

    def post(self, request, pk):
        """Handle http post request"""
        action_key = request.POST.get("action")
        _, method = self.actions[action_key]
        getattr(self, method)()
        return HttpResponseRedirect(reverse("event_admin", kwargs={"pk": pk}))

    def register_user(self):
        """Melder på brukeren nevnt i POST['text'] på arrangementet."""
        username = self.request.POST.get("text")

        # Tar inn verdien True fra checkboksen hvis den er markert
        if self.request.POST.get("Regelboks") == "True":
            regelbryting = True
        else:
            regelbryting = False

        if not username:
            self.messages.warning("Ingen brukernavn skrevet inn.")
            return
        try:
            user = User.objects.get(username=username)

            # Legger brukeren i listen.
            self.get_object().register_user(user, ignore_restrictions=regelbryting)
        except (User.DoesNotExist, UserRegistrationException) as ex:
            self.messages.warning(
                f"Kunne ikke legge til {username} i påmeldingslisten. "
                f"Returnert error var: {type(ex).__name__}: {str(ex)}. "
                "Ta kontakt med WebKom, og oppgi denne feilmeldingen "
                "dersom du tror dette er en feil."
            )

    def deregister_users(self):
        """Melder av brukerne nevnt i POST['user']."""
        user_list = self.request.POST.getlist("user")
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
                    "dersom du tror dette er en feil."
                )


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

    events = Event.objects.filter(event_start__year=year, event_start__month=month)
    cal = EventCalendar(events, year, month).formatmonth(year, month)

    user = request.user
    future_attending_events = attending_events(user, today)

    months = year * 12 + month - 1  # months since epoch (Christ)
    month_list = [
        datetime.date(m // 12, m % 12 + 1, 1) for m in range(months - 5, months + 7)
    ]

    # Get some random dates in the current, next, and previous month.
    # These dates are used load the calendar for that month.
    # * prev is some day in the previous month
    # * this is some day in this month
    # * next is some day in the next month
    context = {
        "calendar": mark_safe(cal),
        "prev": first_of_month - datetime.timedelta(27),
        "this": first_of_month,
        "next": first_of_month + datetime.timedelta(32),
        "future_attending_events": future_attending_events,
        "month_list": month_list,
    }

    return render(request, "events/event_list.html", context)


class EventMainPage(ListView):
    model = Event
    template_name = "events/event_main_page.html"
    NUMBER_OF_EVENTS = 10  # Number of events to list

    def get_queryset(self):
        events = super().get_queryset().order_by("event_start")
        data = (
            self.request.GET
            if self.request.GET
            else {"start_time": datetime.date.today()}
        )
        filterForm = FilterEventsForm(data)
        if filterForm.is_valid():
            if filterForm.cleaned_data["type"] == "event":
                events = events.exclude(is_bedpres=True)
            elif filterForm.cleaned_data["type"] == "bedpres":
                events = events.filter(is_bedpres=True)
            if filterForm.cleaned_data["start_time"]:
                filter_time = filterForm.cleaned_data["start_time"]
            else:
                filter_time = datetime.date.today()
            events = events.filter(event_start__gte=filter_time)

        self.filterForm = filterForm
        events = events[: self.NUMBER_OF_EVENTS]
        return events

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context["penalties"] = user.get_penalties()
            context["penalties__count"] = sum(
                [reg.penalty for reg in context["penalties"]]
            )
            context["user_events"] = user.eventregistration_set.filter(
                event__event_start__gte=datetime.date.today()
            ).order_by("event__event_start")
        context["filter_form"] = self.filterForm
        return context


class EventRegistrationsView(PermissionRequiredMixin, DetailView):
    """Viser en liste over alle brukere påmeldt til arrangementet."""

    model = Event
    context_object_name = "event"
    template_name = "events/event_registrations.html"
    permission_required = "events.add_event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        regs = event.eventregistration_set
        context["eventregistrations"] = regs.order_by("-attending", "user__last_name")
        return context


class EventDetailView(AdminLinksMixin, MessageMixin, DetailView):
    """Viser arrangementet."""

    model = Event
    context_object_name = "event"
    template_name = "events/event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        user = self.request.user

        if user.is_authenticated:
            # Innlogget, så sjekk om de er påmeldt
            try:
                context["is_registered"] = event.is_registered(user)
                context["is_attending"] = event.is_attending(user)
                context["is_waiting"] = event.is_waiting(user)
            except EventException as e:
                self.messages.error(e)

        if event.registration_required and self.request.user.is_authenticated:
            classnumber = [group.get_class_number() for group in event.open_for.all()]
            classnumber = set(classnumber)
            context["classnumber"] = classnumber
            context["allowed_to_attend"] = event.allowed_to_attend(
                user
            ) and event.user_penalty_limit(user)
            try:
                event._assert_user_allowed_to_register(user)
            except UserRegistrationException as e:
                context["reason_for_registration_failure"] = str(e)

        # notify users if their card number is missing when registered for an event where it could be used
        if (
            event.get_noshow_penalty() is not None
            and event.get_noshow_penalty()
            and user.ntnu_card_number in [None, ""]
            and event.is_registered(user)
        ):
            card_warning = (
                "Kortnummer ikke registrert. Du kan få problemer med å registrere oppmøte på arrangementet. "
                "Registrer kortnummeret ditt "
            )

            # include her link
            register_card_warning = format_html(
                "{} <a href='{}'>her</a>.", card_warning, reverse("edit_profile"),
            )

            self.messages.warning(register_card_warning)

        context["type"] = (
            "bedpres" if event.is_bedpres else "event"
        )  # Used to include correct template
        return context

    def get_admin_links(self):
        admin_list = []
        if self.object.registration_required:
            admin_list += [
                {
                    "name": "Administrer påmeldinger",
                    "font_awesome": "user",
                    "url": reverse("event_admin", args=[self.object.id]),
                },
                {
                    "name": "Påmeldingsliste",
                    "font_awesome": "list",
                    "url": reverse("event_registrations", args=[self.object.id]),
                },
            ]
        if self.object.registration_required:
            admin_list.append(
                {
                    "name": "Administrer prikker",
                    "font_awesome": "check",
                    "url": reverse("event_administer_penalties", args=[self.object.id]),
                }
            )
        if self.object.registration_required:
            admin_list.append(
                {
                    "name": "Registrer oppmøte",
                    "font_awesome": "user",
                    "url": reverse("event_register_attendance", args=[self.object.id]),
                }
            )
        return admin_list + super().get_admin_links()


class UserEventView(LoginRequiredMixin, TemplateView):
    """Show list of events the logged in user is registered to"""

    template_name = "events/event_showuser.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        context_data["user"] = user
        if user.is_authenticated:
            regs = user.eventregistration_set.all().order_by("event__event_start")
            context_data["eventregistration_list"] = regs
            context_data["is_on_a_waiting_list"] = regs.filter(attending=False).exists()
            context_data["is_attending_an_event"] = regs.filter(attending=True).exists()
        return context_data


class RegisterUserView(LoginRequiredMixin, MessageMixin, DetailView):
    """View for at en bruker skal kunne melde seg av og på."""

    model = Event
    template_name = "events/event_detail.html"

    def post(self, *args, **kwargs):  # pylint: disable=W0613
        """Handle http post request"""
        reg_type = self.request.POST["registration_type"]
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
            return "Du har ikke lov til å melde deg på dette arrangementet. " + str(e)
        except RegistrationNotOpen:
            return "Påmeldingen er ikke åpen."
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


class AdministerPenaltiesView(PermissionRequiredMixin, DetailView, MessageMixin):
    """Used by event admins to register attendance"""

    model = Event
    template_name = "events/administer_penalties.html"
    permission_required = "events.administer"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        attending = EventRegistration.objects.filter(event=self.object, attending=True)
        redirection = redirect(
            self.request.resolver_match.view_name, kwargs.pop("pk", 1)
        )

        for q in request.POST:
            if q.startswith("user_penalty_"):
                pk = q.split("_")[-1]
                penalty_value = request.POST[q]
                reg_req = attending.get(pk=pk)
                if penalty_value == "None":
                    reg_req.penalty = None
                else:
                    reg_req.penalty = penalty_value
                try:
                    reg_req.full_clean()
                    reg_req.save()
                except ValidationError:
                    self.messages.warning(f"Invalid penalty value for {reg_req.user}.")
        return redirection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        registrations = event.eventregistration_set.filter(attending=True)
        context["registrations"] = registrations.order_by("user__last_name")
        return context


class RegisterAttendanceView(PermissionRequiredMixin, DetailView, MessageMixin):
    """Used by event admins to register attendance"""

    model = Event
    template_name = "events/register_attendance.html"
    permission_required = "events.administer"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        identification_string = request.POST.get("identification_string")
        identification_types = request.POST.getlist("identification_type")

        context = {
            "attendance_message": "Noe gikk galt, prøv igjen",
            "status_type": "danger",
        }
        try:
            registration = self.get_registration_by_identification_string(
                identification_string=identification_string,
                identification_types=identification_types,
            )
        except EventRegistration.DoesNotExist:
            context["attendance_message"] = "Fant ikke bruker med påmelding"
            context["status_type"] = "danger"
        except UserNotAttending:
            context["attendance_message"] = "Brukeren er på ventelisten"
            context["status_type"] = "danger"
        except UserAttendanceException:
            context["attendance_message"] = "Fant ikke bruker med påmelding"
            context["status_type"] = "danger"
        else:
            try:
                self.register_user_attendance(registration=registration)
                context[
                    "attendance_message"
                ] = f"Velkommen {registration.user.first_name}"
                context["status_type"] = "success"
            except UserAlreadyRegistered as e:
                reg_datetime = e.eventregistration.attendance_registration
                context["reg_datetime"] = reg_datetime
                context["attendance_message"] = "Oppmøte allerede registrert"
                context["status_type"] = "warning"
            except ValidationError:
                context["attendance_message"] = "Noe gikk galt, prøv igjen"
                context["status_type"] = "danger"
        # hack to get the right colours
        if context["status_type"] in ["danger", "success"]:
            context["text_type"] = "text-light"
        elif context["status_type"] == "warning":
            context["text_type"] = "text-dark"

        context = {**context, **self.get_context_data(**kwargs)}
        return render(
            request, template_name="events/register_attendance.html", context=context
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        registrations = event.eventregistration_set.filter(attending=True)
        context["registrations_not_registered"] = registrations.filter(
            attendance_registration=None
        ).count()
        return context

    def get_registration_by_identification_string(
        self, identification_string, identification_types
    ):
        event = self.get_object()
        num_id_types = len(identification_types)
        for itr, method in enumerate(identification_types, start=1):
            try:
                if method == "username":
                    registration = event.eventregistration_set.get(
                        user__username=identification_string
                    )
                elif method == "ntnu_card" and identification_string.isnumeric():
                    registration = event.eventregistration_set.get(
                        user=NablaUser.objects.get_from_rfid(identification_string)
                    )
                # not implemented jet
                # elif method == "qr_code":
                #     raise UserAttendanceException(identification_string=identification_string, method=method)
                else:
                    continue
            except EventRegistration.DoesNotExist:
                if not itr == num_id_types:
                    continue
                else:
                    raise EventRegistration.DoesNotExist
            if not registration.attending:
                raise UserNotAttending(
                    eventregistration=registration,
                    identification_string=identification_string,
                )
            return registration
        raise UserAttendanceException(identification_string=identification_string)

    def register_user_attendance(self, registration):
        if registration.attendance_registration is not None:
            raise UserAlreadyRegistered(eventregistration=registration)
        else:
            registration.attendance_registration = datetime.datetime.now()
            # Her sjekker man at det ikke finnes prikkregistrering på påmeldingen fra før
            # Det kan også være en løsning at vi setter antall prikekr til maksimalt antall

            if registration.event.get_is_started() and registration.penalty is None:
                registration.penalty = registration.event.get_late_penalty()
            else:
                registration.penalty = registration.event.get_show_penalty()
            registration.full_clean()
            registration.save()


class RegisterNoshowPenaltiesView(PermissionRequiredMixin, DetailView, MessageMixin):
    """
    Når en post blir sendt hit gis det prikk til til dem som ikke er registrert
    """

    model = Event
    template_name = "events/register_attendance.html"
    permission_required = "events.administer"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        event = self.object
        noshow_penalty = event.get_noshow_penalty()
        if not event.get_is_started():
            try:
                event.start_event()
                event.full_clean()
                event.save()
                return redirect("event_register_attendance", kwargs.pop("pk", 1))
            except EventNotStartedException:
                self.messages.warning("Du kan ikke starte arrangementet før startiden")
            except ValidationError:
                self.messages.warning("Noe gikk galt")
        elif not event.penalties_finished_distributed():
            try:
                if noshow_penalty is None:
                    self.messages.info(
                        "Arrangementet gir ikke prikk for å ikke møte opp. Ingen prikker ble fordelt"
                    )
                elif not event.get_is_started():
                    self.messages.warning(
                        "Du kan ikke gi prikk for manglende oppmøte før arrangementet har begynt!"
                    )
                else:
                    event.eventregistration_set.filter(attending=True).filter(
                        penalty=None
                    ).filter(attendance_registration=None).update(
                        penalty=noshow_penalty
                    )
                    return redirect("event_administer_penalties", kwargs.pop("pk", 1))
            except ValidationError:
                self.messages.warning("Noe gikk galt")
        return redirect("event_register_attendance", kwargs.pop("pk", 1))


def ical_event(request, event_id):
    """Returns a given event or bedpres as an iCal .ics file"""

    event = Event.objects.get(id=event_id)

    # Use the same template for both Event and BedPres.
    template = loader.get_template("events/event_icalendar.ics")
    context = {
        "event_list": (event,),
    }
    response = HttpResponse(template.render(context), content_type="text/calendar")
    response["Content-Disposition"] = "attachment; filename=Nabla_%s.ics" % event.slug
    return response
