# -*- coding: utf-8 -*-

from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.template import loader, Context
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.messages.api import MessageFailure
from django.contrib.auth import get_user_model; User = get_user_model()
from django.contrib.auth.models import UserManager
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.decorators import login_required

from .forms import UserForm, RegistrationForm, SearchForm
from .models import NablaUser

import datetime

## Brukerprofil
class UserDetailView(DetailView):
    """Viser brukerens profil."""
    context_object_name = 'member'
    template_name = "accounts/view_member_profile.html"

    def get_object(self, queryset=None):
        member = NablaUser.objects.get(username=self.kwargs['username'])
        return member

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        member = self.object
        context['see_penalty'] = self.request.user.has_perm('bedpress.change_BedPres') or self.request.user == member
        context['penalty_list'] = member.eventpenalty_set.all()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserDetailView, self).dispatch(*args, **kwargs)


class UpdateProfile(UpdateView):
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UpdateView, self).dispatch(*args, **kwargs)


@login_required
def list(request):
    """Lister opp brukere med pagination."""
    users = NablaUser.objects.all().prefetch_related('groups')

    return render(request, "accounts/list.html", {'users': users})


@login_required
def search(request):
    """ Returnerer brukerne med brukernavn, fornavn eller etternavn som
        begynner på query """

    from django.db.models import Q

    if not (request.method == 'POST'):
        return HttpResponsePermanentRedirect("/brukere/view")
    
    form = SearchForm(request.POST)
        
    if form.is_valid():
        query = form.cleaned_data['searchstring']

        users = NablaUser.objects.filter(Q(username__istartswith=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
        return render(request, "accounts/list.html", {'users': users, 'searchquery': query})
    else:
        return HttpResponsePermanentRedirect("/brukere/view")

def get_name(ntnu_username):
    regex = '^%s:' % username
    process = subprocess.Popen(['grep',regex, settings.NTNU_PASSWD], shell=False, stdout=subprocess.PIPE)
    full_name = process.communicate()[0].split(':')[4].split(" ")
    last_name = full_name.pop()
    first_name = " ".join(full_name)
    return (first_name,last_name)


def user_register(request):
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'] 
            studmail = username+"@stud.ntnu.no"
            (user, created_user) = NablaUser.objects.get_or_create(username=username)

            # At en aktivbruker kommer seg hit skal ikke skje. Dette skal skjekkes i forms
            if user.is_active and user.date_joined.date == datetime.date.today():
                raise Exception
            

            if not(user.email):
                user.email = studmail
            user_manager = UserManager()
            password = user_manager.make_random_password()
            user.set_password(password)
            user.is_active = True
            user.save() 
            t = loader.get_template('accounts/registration_email.txt')
            email_text = t.render(Context(locals()))
            user.email_user('Bruker på nabla.no',email_text)

            messages.add_message(request, messages.INFO, 'Registreringsepost sendt til %s' % user.email)

            return redirect('/')
    else:
        form = RegistrationForm()
    
    return render(request,"accounts/user_registration.html",
                               {'form':form}
                               )


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
