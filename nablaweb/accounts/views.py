# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404, render
from django.template import RequestContext
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from accounts.forms import LoginForm, UserForm, ProfileForm, RegistrationForm
from accounts.models import UserProfile
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage


## Login/logout

@require_http_methods(['POST','GET'])
def login_user(request):
    if request.method == 'GET':
        return login_get(request)
    elif request.method == 'POST':
        return login_post(request)
    else:
        raise Http404

@require_GET
def login_get(request):
    login_form = LoginForm()
    return render_to_response('accounts/login.html', 
                                {'login_form': login_form}, 
                                context_instance=RequestContext(request))
@require_POST
def login_post(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    
    #Hvis bruker ble autentisert log inn og 
    if user is not None and user.is_active:
        login(request,user)
        messages.add_message(request, messages.INFO, 'Du ble logget inn')
        return redirect(request.META.get('HTTP_REFERER','/'))
    else:
        login_form = LoginForm({'username':username})
        messages.add_message(request, messages.ERROR, 'Feil brukernavn/passord!')

        return render_to_response('accounts/login.html', 
                                    {'login_form': login_form}, 
                                    context_instance=RequestContext(request))

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


    return render_to_response("accounts/edit_profile.html", {'userForm': userForm, 'profileForm': profileForm }, context_instance=RequestContext(request))

@login_required
def list(request):
    """Lister opp brukere med pagination."""
    user_list = User.objects.all()
    paginator = Paginator(user_list, 20) # Antall brukere per side 
	
	# Sjekk om brukeren har valgt side
    try: 
		page = int(request.GET.get('side'))
    except:
        # Start på side 1 hvis siden ikke er valgt
        page = 1

	
    # Prøv å hente en den valgte siden
    try:
        users = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # Hent den siste siden om siden ikke er gyldig
        users = paginator.page(paginator.num_pages)
    return render_to_response("accounts/list.html", 
							  {'users': users}, 
							  context_instance=RequestContext(request)
							 )


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return HttpResponse("Riktig")
    else:
        form = RegistrationForm()
    
    return render_to_response("accounts/user_registration.html",
                               {'form':form},
                               context_instance=RequestContext(request)
                               )
def registration_confirmaiton_email(request, username):
    return HttpResponse("")
