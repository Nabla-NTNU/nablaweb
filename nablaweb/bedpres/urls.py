# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from nablaweb.bedpres.models import BedPres
from nablaweb.bedpres.forms import BedPresForm, BedPresFormPreview
from nablaweb.bedpres.views import BedPresDetailView, BedPresListView, BedPresDeleteView, UserBedPresView


urlpatterns = patterns('nablaweb.bedpres.views',

    # Administrasjon
    (r'^opprett/$', BedPresFormPreview(form=BedPresForm)),
    (r'^(?P<pk>\d{1,8})/endre$', BedPresFormPreview(form=BedPresForm)),
    (r'^(?P<pk>\d{1,8})/slette$', BedPresDeleteView.as_view()),
    url(r'^(?P<pk>\d{1,8})/admin$',
        'administer',
        name='bedpres_admin'),
 
    # Offentlig
    url(r'^$',
        BedPresListView.as_view(),
        name='bedpres_list'),
    url(r'^(?P<pk>\d{1,8})/$',
        BedPresDetailView.as_view(),
        name='bedpres_detail'),

    # Bruker
    (r'^mine$', UserBedPresView.as_view()),
    (r'^(?P<bedpres_id>\d{1,8})/registrering$', 'register_user'),

    # Eksporter
    (r'^(?P<bedpres_id>\d{1,8})/eksporter$', 'ical_event'),
)
