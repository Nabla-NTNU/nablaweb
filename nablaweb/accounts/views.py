# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from accounts.forms import LoginForm, UserForm, ProfileForm
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
    if user is not None:
        login(request,user)
        messages.add_message(request, messages.INFO, 'Du ble logget inn')
        if request.META.has_key('HTTP_REFERER'):
            return redirect(request.META['HTTP_REFERER'])
        else:
            redirect("/")
    else:
        login_form = LoginForm({'username':username})
        messages.add_message(request, messages.ERROR, 'Feil brukernavn/passord!')

        return render_to_response('accounts/login.html', 
                                    {'login_form': login_form}, 
                                    context_instance=RequestContext(request))

def logout_user(request):
    messages.add_message(request, messages.INFO, 'Logget ut')
    logout(request)
    
    if request.META.has_key('HTTP_REFERER'):
        return redirect(request.META['HTTP_REFERER'])
    else:
         redirect("/")


## Brukerprofil 
@login_required
def view_member_profile(request, username):
    member = get_object_or_404(User, username=username)
    return render_to_response("accounts/view_member_profile.html", {'member': member}, context_instance=RequestContext(request))
    

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
            messages.add_message(request, messages.INFO, 'Du har skrevet inn noe feil.')


    return render_to_response("accounts/edit_profile.html", {'userForm': userForm, 'profileForm': profileForm }, context_instance=RequestContext(request))

@login_required
def list(request):

	u"""Lister opp brukere med pagination."""

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
	
