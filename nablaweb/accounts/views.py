# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from accounts.forms import LoginForm, UserForm, ProfileForm
from accounts.models import UserProfile
from django.contrib import messages

## Login/logout
def login_user(request):
    if request.method == 'GET':
        return login_get(request)
    elif request.method == 'POST':
        return login_post(request)
    else:
        raise Http404

def login_get(request):
    login_form = LoginForm()
    return render_to_response('accounts/login.html', 
                                {'login_form': login_form}, 
                                context_instance=RequestContext(request))

def login_post(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request,user)
        messages.add_message(request, messages.INFO, 'Du ble logget inn')
        return redirect("/")
    else:
        login_form = LoginForm({'username':username})
        messages.add_message(request, messages.ERROR, 'Feil brukernavn/passord!')

        return render_to_response('accounts/login.html', 
                                    {'login_form': login_form}, 
                                    context_instance=RequestContext(request))

def logout_user(request):
    messages.add_message(request, messages.INFO, 'Logget ut')
    logout(request)
    return redirect("/")


## Brukerprofil 
def view_member_profile(request, username):
    member = get_object_or_404(User, username=username)
    return render_to_response("accounts/view_member_profile.html", {'member': member}, context_instance=RequestContext(request))
    
def edit_profile(request):
    user = request.user;
    updated = False

    # TODO: Lag bedre løsning for ikke innlogget
    if  not(user.is_authenticated()):
        return HttpResponseRedirect("/login/")

    
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
            updated = True
    return render_to_response("accounts/edit_profile.html", {'userForm': userForm, 'profileForm': profileForm, 'updated':updated}, context_instance=RequestContext(request))


