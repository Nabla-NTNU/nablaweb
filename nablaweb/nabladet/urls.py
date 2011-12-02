from django.conf.urls.defaults import *
from nabladet.views import NabladListView, NabladDetailView

urlpatterns = patterns('nablad.views',
    # Offentlig
    url(r'^$', NabladListView.as_view(), name='nablad_list'),
    url(r'^(?P<pk>\d{1,8})/$', NabladDetailView.as_view(), name='nablad_detail'),
)
