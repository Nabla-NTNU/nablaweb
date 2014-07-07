# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic import RedirectView

urlpatterns = patterns('django.contrib.auth.views', 
    url(r'password/change/$', 'password_change', name='password_change'),
    url(r'password/change/done$', 'password_change_done', name='password_change_done'),
    (r'password/reset/$', 'password_reset'),
    (r'password/reset/done/$', 'password_reset_done'),
    (r'password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
    (r'password/reset/complete/$', 'password_reset_complete'),
)

urlpatterns += patterns('accounts.views',
    (r'edit/$', 'edit_profile'),
    (r'view/$', 'list'),
    (r'^$', RedirectView.as_view(url='view/')),
    url(r'view/(?P<username>\w+)/$', 'view_member_profile', name='profile_link'),
    url(r'register/$', 'user_register', name='registration_register'),
    url(r'search/$', 'search', name='user_search'),
#    (r'test/', DetailView.as_view(model=User, id=1)),
)
