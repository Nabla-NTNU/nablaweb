# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *


urlpatterns = patterns('django.contrib.auth.views',
    (r'password_reset/$', 'password_reset'),
    (r'password_reset_done/$', 'password_reset_done'),
    (r'password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
    (r'password_reset_complete/$', 'password_reset_complete'),
)

