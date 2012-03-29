# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('django.contrib.auth.views',
    (r'password/reset/$', 'password_reset'),
    (r'password/reset/done/$', 'password_reset_done'),
    (r'password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
    (r'password/reset/complete/$', 'password_reset_complete'),
)

urlpatterns += patterns('nablaweb.accounts.views',
    (r'edit/$', 'edit_profile'),
    (r'view/$', 'list'),
    (r'view/(?P<username>\w+)/$', 'view_member_profile'),
    url(r'register/$', 'user_register', name='registration_register'),
    (r'search/(?P<query>\w+)/$', 'search'),
#    (r'test/', DetailView.as_view(model=User, id=1)),
)
