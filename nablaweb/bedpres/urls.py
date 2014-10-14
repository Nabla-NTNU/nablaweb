# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.views.generic import RedirectView

from events.views import ical_event

from .models import BedPres
from .views import *

urlpatterns = patterns('bedpres.views',

    # Administrasjon
    (r'^opprett/$', BPCFormView.as_view()),

    url(r'^$', RedirectView.as_view(url='/arrangement/')),
    url(r'^(?P<pk>\d{1,8})-(?P<slug>[-\w]*)$',
        BedPresDetailView.as_view( context_object_name = "bedpres" ),
        name='bedpres_detail'),

    # Bruker
    (r'^registration', 'registration'),
    (r'^(?P<bedpres_id>\d{1,8})/registration', 'registration'),

    # Eksporter
    (r'^(?P<bedpres_id>\d{1,8})/eksporter$', ical_event),
)
