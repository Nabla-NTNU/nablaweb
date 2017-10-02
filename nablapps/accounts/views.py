from braces.views import (
    FormMessagesMixin,
    LoginRequiredMixin,
    MessageMixin,
    PermissionRequiredMixin,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, UpdateView, FormView, TemplateView

from .forms import UserForm, RegistrationForm, InjectUsersForm
from .models import NablaUser, NablaGroup, RegistrationRequest
from .utils import activate_user_and_create_password, send_activation_email, extract_usernames

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    """Viser brukerens profil."""
    context_object_name = 'member'
    template_name = "accounts/view_member_profile.html"

    def get_object(self, queryset=None):
        try:
            view_user = NablaUser.objects.get(username=self.kwargs['username'])
        except NablaUser.DoesNotExist:
            raise Http404("Bruker finnes ikke")
        return view_user


class UpdateProfile(LoginRequiredMixin, FormMessagesMixin, UpdateView):
    form_class = UserForm
    template_name = 'accounts/edit_profile.html'
    form_valid_message = 'Profil oppdatert.'
    form_invalid_message = 'Du har skrevet inn noe feil.'

    def get_object(self, queryset=None):
        return self.request.user


class UserList(LoginRequiredMixin, ListView):
    queryset = NablaUser.objects.filter(is_active=True)\
                        .prefetch_related('groups')\
                        .order_by('username')
    context_object_name = 'users'
    template_name = 'accounts/list.html'


class RegistrationView(MessageMixin, FormView):
    form_class = RegistrationForm
    template_name = 'accounts/user_registration.html'
    success_url = '/login/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')

        # Activate a user or create a registration request.
        try:
            user = NablaUser.objects.get(username=username)
            if user.is_active:
                self.messages.error("Denne brukeren er allerede aktivert.")
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                password = activate_user_and_create_password(user)
                send_activation_email(user, password)
                self.messages.info("Registreringsepost sendt til {}".format(user.email))
        except NablaUser.DoesNotExist:
            RegistrationRequest.objects.create(
                    username=username,
                    first_name=first_name,
                    last_name=last_name
            )
            self.messages.info("Denne brukeren er ikke registrert. "
                               "En forespørsel har blitt opprettet og "
                               "du vil få en epost hvis den blir godkjent.")
        return super(RegistrationView, self).form_valid(form)


class InjectUsersFormView(LoginRequiredMixin, FormMessagesMixin, FormView):
    form_class = InjectUsersForm
    form_valid_message = "Brukerne er lagt i databasen."
    form_invalid_message = "Ikke riktig utfyllt."
    template_name = 'form.html'
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_module_perms("django.contrib.auth"):
            return super(InjectUsersFormView, self).dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()

    def form_valid(self, form):
        data = form.cleaned_data['data']
        extract_usernames(data)
        return super(InjectUsersFormView, self).form_valid(form)


class BirthdayView(LoginRequiredMixin, ListView):
    allow_empty = True
    date_field = "birthday"
    template_name = "accounts/user_birthday.html"
    context_object_name = "users"

    def get_queryset(self):
        return NablaUser.objects.filter_has_birthday_today()


class MailListView(PermissionRequiredMixin, TemplateView):
    template_name = 'accounts/mail_list.html'
    permission_required = 'accounts.change_nablagroup'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        group_ids = {int(i) for i in self.kwargs['groups'].split('/')}
        groups = NablaGroup.objects.filter(id__in=group_ids)
        context["users"] = NablaUser.objects.filter(groups__in=groups)
        context["groups"] = groups
        return context
