# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from nablaweb.bedpres.models import BedPres
from nablaweb.bedpres.forms import BedPresForm
from nablaweb.bedpres.views import BedPresDetailView, BedPresListView, BedPresDeleteView, UserBedPresView, BPCFormView
from django.views.generic.simple import redirect_to


urlpatterns = patterns('nablaweb.bedpres.views',

    # Administrasjon
    (r'^opprett/$', BPCFormView.as_view()),
#    (r'^(?P<pk>\d{1,8})/endre$', BedPresFormPreview(form=BedPresForm)),
#    (r'^(?P<pk>\d{1,8})/slette$', BedPresDeleteView.as_view()),
    url(r'^(?P<pk>\d{1,8})/admin$',
        'administer',
        name='bedpres_admin'),
 
    # Offentlig
    #url(r'^$',
    #    BedPresListView.as_view( context_object_name = "bedpres_list" ),
    #    name='bedpres_list'),
    (r'^$', redirect_to, {'url': '/arrangement/'}),
    url(r'^(?P<pk>\d{1,8})-(?P<slug>[-\w]*)$',
        BedPresDetailView.as_view( context_object_name = "bedpres" ),
        name='bedpres_detail'),

    # Bruker
    (r'^mine$', UserBedPresView.as_view()),
    (r'^(?P<bedpres_id>\d{1,8})/avregistrering/$', 'deregister_user'),
    (r'^(?P<bedpres_id>\d{1,8})/registrering/$', 'register_user'),

    # Eksporter
    (r'^(?P<bedpres_id>\d{1,8})/eksporter$', 'ical_event'),
)
