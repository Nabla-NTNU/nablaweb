# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from django.views.generic import ListView
from accounts.models import UserProfile


<<<<<<< HEAD
urlpatterns = patterns('django.contrib.auth.views',
    (r'password_reset/$', 'password_reset'),
    (r'password_reset_done/$', 'password_reset_done'),
    (r'password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
    (r'password_reset_complete/$', 'password_reset_complete'),
=======
urlpatterns = patterns('nablaweb.accounts.views',
	(r'list/', 'list'),
    (r'view/(?P<username>\w+)/', 'view_member_profile')
>>>>>>> b58829b709a4abffdf9fbe3940b690efc0898536
)

