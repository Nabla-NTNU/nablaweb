import re

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from braces.views import (
    FormMessagesMixin,
    LoginRequiredMixin,
    MessageMixin,
    PermissionRequiredMixin,
)

from .forms import ConfirmUsersForm, RegistrationForm, UserForm
from .models import FysmatClass, NablaGroup, NablaUser, RegistrationRequest

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    """Viser brukerens profil."""

    context_object_name = "member"
    template_name = "accounts/view_member_profile.html"

    def get_object(self, queryset=None):
        try:
            view_user = NablaUser.objects.get(username=self.kwargs["username"])

            # Folk lagrer med og uten protokoll - må normaliseres for å funke
            if view_user.web_page:
                view_user.web_page = view_user.web_page.removeprefix("http://")
                view_user.web_page = view_user.web_page.removeprefix("https://")

        except NablaUser.DoesNotExist:
            raise Http404("Bruker finnes ikke")
        return view_user


class UpdateProfile(LoginRequiredMixin, FormMessagesMixin, UpdateView):
    form_class = UserForm
    template_name = "accounts/edit_profile.html"
    form_valid_message = "Profil oppdatert."
    form_invalid_message = "Du har skrevet inn noe feil."

    def get_object(self, queryset=None):
        return self.request.user


class UserList(LoginRequiredMixin, ListView):
    queryset = (
        NablaUser.objects.filter(is_active=True)
        .prefetch_related("groups")
        .order_by("username")
    )
    context_object_name = "users"
    template_name = "accounts/list.html"
    paginate_by = 20
    page_kwarg = "side"


class RegistrationView(MessageMixin, FormView):
    form_class = RegistrationForm
    template_name = "accounts/user_registration.html"
    success_url = "/login/"

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        class_name = form.cleaned_data.get("fysmat_class")
        fysmat_class = FysmatClass.objects.get(name=class_name)

        # Activate a user or create a registration request.
        try:
            user = NablaUser.objects.get(username=username)
            if user.is_active:
                self.messages.error("Denne brukeren er allerede aktivert.")
            else:
                user.first_name = first_name
                user.last_name = last_name
                fysmat_class.user_set.add(user)
                user.activate()
                self.messages.info(f"Registreringsepost sendt til {user.email}")

        except NablaUser.DoesNotExist:
            RegistrationRequest.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                fysmat_class=fysmat_class,
            )
            self.messages.warning(
                "Denne brukeren er ikke registrert. "
                "En forespørsel har blitt opprettet og "
                "du vil få en epost hvis den blir godkjent."
            )
        return super().form_valid(form)


class ConfirmUsersFormView(PermissionRequiredMixin, FormMessagesMixin, FormView):
    form_class = ConfirmUsersForm
    form_valid_message = "Brukerne er lagt i databasen."
    form_invalid_message = "Ikke riktig utfyllt."
    template_name = "accounts/confirmation.html"
    permission_required = "accounts.change_registrationrequest"

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["requests"] = RegistrationRequest.objects.all().order_by("-created")
        context["unpaid_users"] = NablaUser.objects.filter(
            Q(password__startswith="!")
        ).order_by("-date_joined")
        return context

    def form_valid(self, form):
        from .models import FysmatClass

        usernames_string = form.cleaned_data["data"]
        usernames = re.findall(
            r"^([a-zæøå]+[1-9]*)\s*$",
            usernames_string,
            flags=re.IGNORECASE | re.MULTILINE,
        )
        for username in usernames:
            users = NablaUser.objects.filter(username=username)
            if users.exists():
                self.messages.info(f"Bruker {username} eksisterer allerede!")
                continue

            requests = RegistrationRequest.objects.filter(username=username)
            if requests.exists():
                requests[0].approve_request()
                self.messages.success(f"Aktivert bruker {username}")
            else:
                user = NablaUser.objects.create_user(username=username)
                send_mail(
                    subject="Velkommen til nabla!",
                    message="""Hei!

Vi har registrert et betalt kontigent fra deg, og har derfor laget deg en bruker på nabla.no. Så snart du fyller ut skjema på https://nabla.no/brukere/registrer/ kan du logge inn!

Velkommen til oss,
-Oss i Nablas WebKomité
""",
                    from_email="noreply@nabla.no",
                    recipient_list=[user.email],
                )
                user.is_active = False
                user.save()
                self.messages.info(f"Laget skall-bruker for {username}")
        return super().form_valid(form)


class BirthdayView(LoginRequiredMixin, ListView):
    allow_empty = True
    date_field = "birthday"
    template_name = "accounts/user_birthday.html"
    context_object_name = "users"

    def get_queryset(self):
        return NablaUser.objects.filter_has_birthday_today()


class MailListView(PermissionRequiredMixin, TemplateView):
    template_name = "accounts/mail_list.html"
    permission_required = "accounts.change_nablagroup"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        group_ids = {int(i) for i in self.kwargs["groups"].split("/")}
        groups = NablaGroup.objects.filter(id__in=group_ids)
        context["users"] = NablaUser.objects.filter(groups__in=groups)
        context["groups"] = groups
        return context
