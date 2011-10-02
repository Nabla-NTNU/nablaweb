# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from django.views.generic import ListView
from accounts.models import UserProfile


urlpatterns = patterns('django.contrib.auth.views',
    (r'password/reset/$', 'password_reset'),
    (r'password/reset/done/$', 'password_reset_done'),
    (r'password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
    (r'password/reset/complete/$', 'password_reset_complete'),
)

urlpatterns += patterns('nablaweb.accounts.views',
	(r'list/', 'list'),
    (r'view/(?P<username>\w+)/', 'view_member_profile'),
    (r'register/','user_register'),
)

