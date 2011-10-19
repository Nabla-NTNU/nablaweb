# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404, render
from django.template import RequestContext, loader, Context
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User, UserManager
from accounts.forms import LoginForm, UserForm, ProfileForm, RegistrationForm
from accounts.models import UserProfile
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

import datetime

## Login/logout

@require_http_methods(['POST','GET'])
def login_user(request):
    redirect_to = request.REQUEST.get('next',request.META.get('HTTP_REFERER','/'))
    if request.user.is_authenticated():
        return redirect(redirect_to)


    if request.method == 'GET':
        login_form = LoginForm()
    elif request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        #Hvis bruker ble autentisert log inn og 
        if user is not None and user.is_active:
            login(request,user)
            messages.add_message(request, messages.INFO, 'Du ble logget inn')
            return redirect(redirect_to)
        else:
            login_form = LoginForm({'username':username})
            messages.add_message(request, messages.ERROR, 'Feil brukernavn/passord!')

    return render(request,'accounts/login.html', 
                                {'login_form': login_form,
                                  'next': redirect_to} 
                                )

def logout_user(request):
    messages.add_message(request, messages.INFO, 'Logget ut')
    logout(request)
    return redirect(request.META.get('HTTP_REFERER','/'))



## Brukerprofil 
@login_required
def view_member_profile(request, username=None):

    """Viser profilen til en oppgitt bruker. Om brukernavn ikke er oppgitt
    vises profilen til brukeren selv."""

    if username:
        member = get_object_or_404(User, username=username)
    else:
        member = request.user
    return render(
        request, "accounts/view_member_profile.html", 
        {'member': member})
    # Render er identisk med render_to_response, men tar request som første
    # argument istedenfor RequestContext(request) som tredje argument.
    # Importeres fra django.shortcuts
    

@login_required
def edit_profile(request):
    user = request.user;
    updated = False

    userProfile = UserProfile.objects.get_or_create(user=user)[0]
    
    if request.method == 'GET': 
        userForm = UserForm(instance=user)
        profileForm = ProfileForm(instance=userProfile)
    elif request.method == 'POST':
        userForm = UserForm(request.POST, instance=user)
        profileForm = ProfileForm(request.POST, instance=userProfile)
        if userForm.is_valid() and profileForm.is_valid() :
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
def list(request, year=None):
    """Lister opp brukere med pagination."""
    users = User.objects.all()
	
    return render(request,"accounts/list.html", 
							  {'users': users} 
							 )



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

