# -*- coding: utf-8 -*-

# URL-er for com-appen

from django.conf.urls.defaults import *
from com.views import *
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    (r'^$', redirect_to, {'url': '/'}),
)
