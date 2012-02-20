# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from nablaweb.bedpres.models import BedPres
from nablaweb.bedpres.forms import BedPresForm
from nablaweb.bedpres.views import BedPresDetailView, BedPresListView, BedPresDeleteView, UserBedPresView, BedPresSelectFromBPC


urlpatterns = patterns('nablaweb.bedpres.views',

    # Administrasjon
#    (r'^opprett/(?P<bpcid>\d{1,8})$', BedPresFormPreview(form=BedPresForm)),
#    (r'^opprett/velg$', BedPresSelectFromBPC.as_view()),
#    (r'^(?P<pk>\d{1,8})/endre$', BedPresFormPreview(form=BedPresForm)),
#    (r'^(?P<pk>\d{1,8})/slette$', BedPresDeleteView.as_view()),
    url(r'^(?P<pk>\d{1,8})/admin$',
        'administer',
        name='bedpres_admin'),
 
    # Offentlig
    url(r'^$',
        BedPresListView.as_view( context_object_name = "bedpres_list" ),
        name='bedpres_list'),
    url(r'^(?P<pk>\d{1,8})/$',
        BedPresDetailView.as_view( context_object_name = "bedpres" ),
        name='bedpres_detail'),

    # Bruker
    (r'^mine$', UserBedPresView.as_view()),
    (r'^(?P<bedpres_id>\d{1,8})/registrering$', 'register_user'),

    # Eksporter
    (r'^(?P<bedpres_id>\d{1,8})/eksporter$', 'ical_event'),
)
