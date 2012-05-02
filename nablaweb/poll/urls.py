# -*- coding: utf-8 -*-

# URL-er for stillingsannonser-appen

from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
#    (r'^$', redirect_to, {'url', '/'}),
    (r'^(?P<poll_id>\d+)/vote/$', 'poll.views.vote'),
)
