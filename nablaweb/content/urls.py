# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from nablaweb.content.views import ContentListView  # , ContentDeleteView

urlpatterns = patterns('content.views',

    # Administrasjon
#    (r'^opprett/$', ContentFormPreview(form=ContentForm)),
#    (r'^(?P<pk>\d{1,8})/endre/$', ContentFormPreview(form=ContentForm)),
#    (r'^(?P<pk>\d{1,8})/slette/$', ContentDeleteView.as_view()),

    # Offentlig
    url(r'^$',
        ContentListView.as_view(),
        name='content_list'),
)
