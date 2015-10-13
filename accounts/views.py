# -*- coding: utf-8 -*-

from django.views.generic import DetailView, ListView, UpdateView, FormView
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from braces.views import LoginRequiredMixin, FormMessagesMixin, MessageMixin
import datetime

from .forms import UserForm, RegistrationForm, InjectUsersForm
from .models import NablaUser
from .utils import activate_user_and_create_password, send_activation_email, extract_usernames

User = get_user_model()


#  Brukerprofil
class UserDetailView(LoginRequiredMixin, DetailView):
    """Viser brukerens profil."""
    context_object_name = 'member'
    template_name = "accounts/view_member_profile.html"

    def get_object(self, queryset=None):
        return NablaUser.objects.get(username=self.kwargs['username'])


class UpdateProfile(LoginRequiredMixin, FormMessagesMixin, UpdateView):
    form_class = UserForm
    template_name = 'accounts/edit_profile.html'
    form_valid_message = 'Profil oppdatert.'
    form_invalid_message = 'Du har skrevet inn noe feil.'

    def get_object(self, queryset=None):
        return self.request.user


class UserList(LoginRequiredMixin, ListView):
    queryset = NablaUser.objects.filter(is_active=True).prefetch_related('groups').order_by('username')
    context_object_name = 'users'
    template_name = 'accounts/list.html'


class RegistrationView(MessageMixin, FormView):
    form_class = RegistrationForm
    template_name = 'accounts/user_registration.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data['username'] 
        user, created_user = NablaUser.objects.get_or_create(username=username)

        password = activate_user_and_create_password(user)
        send_activation_email(user, password)

        self.messages.info('Registreringsepost sendt til %s' % user.email)
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


class BirthdayView(ListView):
    model = NablaUser
    allow_empty = True
    date_field = "birthday"
    template_name = "accounts/user_birthday.html"
    context_object_name = "users"

    def get_queryset(self):
        today = datetime.date.today()
        return NablaUser.objects.filter(birthday__day=today.day)

