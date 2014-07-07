# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from events.models import Event
from events.forms import EventForm
from events.views import EventDetailView, EventListView, UserEventView


urlpatterns = patterns('twitter.views',

    #url(r'^tweet$', 'tweet')
 
)
