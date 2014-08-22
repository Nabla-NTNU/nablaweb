# -*- coding: utf-8 -*-

from django.conf.urls import *
from bedpres.models import BedPres
from bedpres.forms import BedPresForm
from bedpres.views import BedPresDetailView, BedPresListView, UserBedPresView, BPCFormView
from django.views.generic import RedirectView

urlpatterns = patterns('bedpres.views',

    # Administrasjon
    (r'^opprett/$', BPCFormView.as_view()),
#    (r'^(?P<pk>\d{1,8})/endre$', BedPresFormPreview(form=BedPresForm)),
    url(r'^(?P<pk>\d{1,8})/admin$',
        'administer',
        name='bedpres_admin'),
 
    # Offentlig
    #url(r'^$',
    #    BedPresListView.as_view( context_object_name = "bedpres_list" ),
    #    name='bedpres_list'),
    url(r'^$', RedirectView.as_view(url='/arrangement/')),
    url(r'^(?P<pk>\d{1,8})-(?P<slug>[-\w]*)$',
        BedPresDetailView.as_view( context_object_name = "bedpres" ),
        name='bedpres_detail'),

    # Bruker
    (r'^mine$', UserBedPresView.as_view()),
    (r'^registration', 'registration'),
    (r'^(?P<bedpres_id>\d{1,8})/registration', 'registration'),

    # Eksporter
    (r'^(?P<bedpres_id>\d{1,8})/eksporter$', 'ical_event'),
)
