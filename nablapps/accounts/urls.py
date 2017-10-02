import django.contrib.auth.views as auth_views
from django.conf.urls import url, include
from django.views.generic import RedirectView
from .views import (
    BirthdayView,
    InjectUsersFormView,
    MailListView,
    RegistrationView,
    UpdateProfile,
    UserDetailView,
    UserList,
)

password_change_patterns = [
    url(r'^$',
        auth_views.password_change,
        name='password_change'),
    url(r'^done$',
        auth_views.password_change_done,
        name='password_change_done'),
]

password_reset_patterns = [
    url(r'^$',
        auth_views.password_reset,
        name='password_reset'),
    url(r'^done/$',
        auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),
]

urlpatterns = [
    url(r'^$',
        RedirectView.as_view(url='view/', permanent=True)),
    url(r'^edit/$',
        UpdateProfile.as_view(),
        name='edit_profile'),
    url(r'^view/$',
        UserList.as_view(),
        name='user_list'),
    url(r'^view/(?P<username>\w+)/$',
        UserDetailView.as_view(),
        name='member_profile'),
    url(r'^registrer/$',
        RegistrationView.as_view(),
        name='user_registration'),
    url(r'^oppdater/$',
        InjectUsersFormView.as_view(),
        name='users_inject'),
    url(r'^bursdag/(?P<day>[0-9]+)?',
        BirthdayView.as_view(),
        name='users_birthday'),
    url(r'^password/change/', include(password_change_patterns)),
    url(r'^password/reset/', include(password_reset_patterns)),
    url(r'^mailliste/(?P<groups>(\d+)(/\d+)*)/$',
        MailListView.as_view(),
        name='mail_list'),
]

# To be imported in the main urls.py
login_urls = [
    url(r'^login/$',
        auth_views.login,
        {'template_name': 'accounts/login.html'},
        name='auth_login'),
    url(r'^logout/$',
        auth_views.logout,
        {'next_page': '/'},
        name='auth_logout'),
]
