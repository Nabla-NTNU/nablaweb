# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from nablaweb.events.models import Event
from nablaweb.events.forms import EventForm
from nablaweb.events.views import EventDetailView, EventListView, EventDeleteView, UserEventView


urlpatterns = patterns('nablaweb.twitter.views',

    #url(r'^tweet$', 'tweet')
 
)
