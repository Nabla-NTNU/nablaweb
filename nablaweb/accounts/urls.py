# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *


urlpatterns = patterns('nablaweb.accounts.views',
	(r'list/', 'list'),
    (r'view/(?P<username>\w+)/', 'view_member_profile')
)
