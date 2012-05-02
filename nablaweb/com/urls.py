# -*- coding: utf-8 -*-

# URL-er for com-appen

from django.conf.urls.defaults import *
from com.views import *
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    (r'^$', redirect_to, {'url': '/'}),
    url(r'^(?P<slug>\D{1,85})/$', ShowPage.as_view(), name='show_com_page'),
)
