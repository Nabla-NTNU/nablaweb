# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from com.views import ShowPage
from django.views.generic import RedirectView

urlpatterns = patterns('',
    (r'^$', RedirectView.as_view(url='/')),
    url(r'^(?P<slug>\D{1,85})/$', ShowPage.as_view(), name='show_com_page'),
)
