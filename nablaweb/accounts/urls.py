# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.views.generic import RedirectView

from .views import UserDetailView

urlpatterns = patterns('django.contrib.auth.views', 
    url(r'password/change/$', 'password_change', name='password_change'),
    url(r'password/change/done$', 'password_change_done', name='password_change_done'),
    (r'password/reset/$', 'password_reset'),
    (r'password/reset/done/$', 'password_reset_done'),
    (r'password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
    (r'password/reset/complete/$', 'password_reset_complete'),
)

urlpatterns += patterns('accounts.views',
    url(r'^$', RedirectView.as_view(url='view/')),
    url(r'edit/$', 'edit_profile'),
    url(r'view/$', 'list'),
    url(r'view/(?P<username>\w+)/$', UserDetailView.as_view(), name='member_profile'),
    url(r'register/$', 'user_register', name='registration_register'),
    url(r'search/$', 'search', name='user_search'),
)
