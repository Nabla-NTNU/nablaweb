from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User

from accounts.forms import LoginForm



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
        return redirect("/")
    else:
        login_form = LoginForm({'username':username})
        return render_to_response('accounts/login.html', 
                                    {'login_form': login_form, 'failed_login':True}, 
                                    context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return redirect("/")

def view_member_profile(request, username):
    member = get_object_or_404(User, username=username)
    return render_to_response("accounts/view_member_profile.html", {'member': member}, context_instance=RequestContext(request))
    
