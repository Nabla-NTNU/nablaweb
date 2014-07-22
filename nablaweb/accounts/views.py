# -*- coding: utf-8 -*-

from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.views.generic import DetailView
from django.template import loader, Context
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.messages.api import MessageFailure
from django.contrib.auth import get_user_model; User = get_user_model()
from django.contrib.auth.models import UserManager
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.decorators import login_required

from .forms import UserForm, ProfileForm, RegistrationForm, SearchForm
from .models import UserProfile

import datetime

## Brukerprofil
class UserDetailView(DetailView):
    """Viser brukerens profil."""
    context_object_name = 'member'
    template_name = "accounts/view_member_profile.html"

    def get_object(self, queryset=None):
        member = User.objects.get(username=self.kwargs['username'])
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


@login_required
def edit_profile(request):
    user = request.user

    userProfile = UserProfile.objects.get_or_create(user=user)[0]

    if request.method == 'GET':
        userForm = UserForm(instance=user)
        profileForm = ProfileForm(instance=userProfile)
    elif request.method == 'POST':
        userForm = UserForm(request.POST, instance=user)
        profileForm = ProfileForm(request.POST, request.FILES, instance=userProfile)
        from pprint import pprint
        pprint(request.FILES)

        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.add_message(request, messages.INFO, 'Profil oppdatert.')
        else:
            messages.add_message(request, messages.ERROR, 'Du har skrevet inn noe feil.')

    return render(request,
        "accounts/edit_profile.html",
        {'userForm': userForm,
          'profileForm': profileForm},
        )


@login_required
def list(request):
    """Lister opp brukere med pagination."""
    users = User.objects.all().prefetch_related('groups')

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

        users = User.objects.filter(Q(username__istartswith=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
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
            (user, created_user) = User.objects.get_or_create(username=username)

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
