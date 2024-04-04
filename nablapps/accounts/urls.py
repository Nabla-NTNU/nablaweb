"""
Urls for accounts app.

Also adds urls from contrib.auth for login, logout,
password change and password reset.
"""

import django.contrib.auth.views as auth_views
from django.urls import include, path, re_path
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
    path("", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path(
        "done",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]

password_reset_patterns = [
    path("", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    re_path(
        r"^confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

urlpatterns = [
    path("", RedirectView.as_view(url="view/", permanent=True)),
    path("edit/", UpdateProfile.as_view(), name="edit_profile"),
    path("view/", UserList.as_view(), name="user_list"),
    path("view/<str:username>/", UserDetailView.as_view(), name="member_profile"),
    path("registrer/", RegistrationView.as_view(), name="user_registration"),
    path("oppdater/", InjectUsersFormView.as_view(), name="users_inject"),
    re_path(
        r"^bursdag/(?P<day>[0-9]+)?", BirthdayView.as_view(), name="users_birthday"
    ),
    path("password/change/", include(password_change_patterns)),
    path("password/reset/", include(password_reset_patterns)),
    re_path(
        r"^mailliste/(?P<groups>(\d+)(/\d+)*)/$",
        MailListView.as_view(),
        name="mail_list",
    ),
]

# To be imported in the main urls.py
login_urls = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="auth_login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="auth_logout"),
]
