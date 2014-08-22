# -*- coding: utf-8 -*-

# URL-er for com-appen

from django.conf.urls import *
from com.views import *
from django.views.generic import RedirectView

urlpatterns = patterns('',
    (r'^$', RedirectView.as_view(url='/')),
    url(r'^(?P<slug>\D{1,85})/$', ShowPage.as_view(), name='show_com_page'),
)
