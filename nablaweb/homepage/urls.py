# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from django.views.generic import ListView
from accounts.models import UserProfile


urlpatterns = patterns('homepage.views',
    (r'^$', 'start'), # Startsiden
)
