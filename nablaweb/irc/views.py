# -*- coding: utf-8 -*-

# Views for irc-appen

from django.template import Context, RequestContext, loader
from django.shortcuts import render

def showChannel(request):
    return render(request, 'irc/default.html')
    
def showChannelStats(request):
    pass

def showTotalStats(request):
    pass
