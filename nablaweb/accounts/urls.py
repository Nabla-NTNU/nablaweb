# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from django.views.generic import ListView
from accounts.models import UserProfile


urlpatterns = patterns('nablaweb.accounts.views',
	(r'list/', 'list'),
    (r'view/(?P<username>\w+)/', 'view_member_profile')
)
