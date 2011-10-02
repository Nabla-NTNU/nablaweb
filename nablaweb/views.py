from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse


def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))


def mail(request):
    request.user.email_user("Test","Jeg tester om epost funker")
    return HttpResponse("hei") 
