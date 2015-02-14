# -*- coding: utf-8 -*-

from django.views.generic import DetailView, ListView, UpdateView, FormView
from django.contrib import messages
from django.contrib.messages.api import MessageFailure
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out

from braces.views import LoginRequiredMixin

from .forms import UserForm, RegistrationForm
from .models import NablaUser
from .utils import activate_user_and_create_password, send_activation_email

User = get_user_model()

## Brukerprofil
class UserDetailView(LoginRequiredMixin, DetailView):
    """Viser brukerens profil."""
    context_object_name = 'member'
    template_name = "accounts/view_member_profile.html"

    def get_object(self, queryset=None):
        return NablaUser.objects.get(username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        return context


class UpdateProfile(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    template_name = 'accounts/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, 'Profil oppdatert.')
        return super(UpdateProfile, self).form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Du har skrevet inn noe feil.')
        return super(UpdateProfile, self).form_invalid(form)


class UserList(LoginRequiredMixin, ListView):
    queryset = NablaUser.objects.filter(is_active=True).prefetch_related('groups').order_by('username')
    context_object_name = 'users'
    template_name = 'accounts/list.html'


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'accounts/user_registration.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data['username'] 
        user, created_user = NablaUser.objects.get_or_create(username=username)

        password = activate_user_and_create_password(user)
        send_activation_email(user, password)

        messages.add_message(self.request,messages.INFO,
                             'Registreringsepost sendt til %s' % user.email)
        return super(RegistrationView, self).form_valid(form)


## Login/logout meldinger
def login_message(sender, request, user, **kwargs):
    try:
        messages.add_message(request, messages.INFO, u'Velkommen inn <strong>{}</strong>'.format(user.username))
    except MessageFailure:
        pass
user_logged_in.connect(login_message)

def logout_message(sender, request, user, **kwargs):
    try:
        messages.add_message(request, messages.INFO, u'<strong>{}</strong> ble logget ut'.format(user.username))
    except MessageFailure:
        pass
user_logged_out.connect(logout_message)
