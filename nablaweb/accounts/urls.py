# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.views.generic import RedirectView

from .views import UserDetailView, UpdateProfile, UserList, RegistrationView

urlpatterns = patterns('django.contrib.auth.views', 
    url(r'password/change/$', 'password_change', name='password_change'),
    url(r'password/change/done$', 'password_change_done', name='password_change_done'),
    url(r'password/reset/$', 'password_reset', name='password_reset'),
    url(r'password/reset/done/$', 'password_reset_done', name='password_reset_done'),
    url(r'password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm', name='password_reset_confirm'),
    url(r'password/reset/complete/$', 'password_reset_complete', name='password_reset_complete'),
)

urlpatterns += patterns('accounts.views',
    url(r'^$',
        RedirectView.as_view(url='view/')),
    url(r'edit/$',
        UpdateProfile.as_view(),
        name='edit_profile'),
    url(r'view/$',
        UserList.as_view(),
        name='user_list'),
    url(r'view/(?P<username>\w+)/$',
        UserDetailView.as_view(),
        name='member_profile'),
    url(r'register/$',
        RegistrationView.as_view(),
        name='user_registration'),
)
