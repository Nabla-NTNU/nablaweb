# -*- coding: utf-8 -*-

# URL-er for stillingsannonser-appen

from django.conf.urls.defaults import *
from django.views.generic import RedirectView

urlpatterns = patterns('',
    (r'^(?P<poll_id>\d+)/vote/$', 'poll.views.vote'),
)
