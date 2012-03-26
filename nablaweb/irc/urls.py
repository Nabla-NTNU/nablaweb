# -*- coding: utf-8 -*-

# URL-er for IRC-appen

from django.conf.urls.defaults import *
from irc.views import *

urlpatterns = patterns('',
    url(r'^$', showChannel, name='irc'),
)
