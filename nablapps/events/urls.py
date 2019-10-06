"""
Urls for events
"""
from django.conf.urls import url
from .views import (
    AdministerRegistrationsView,
    calendar,
    UserEventView,
    RegisterUserView,
    EventDetailView,
    EventRegistrationsView,
    RegisterAttendanceView,
    ical_event,
    EventMainPage
)
from .feeds import RecentEvents

urlpatterns = [
    url(r'^(?P<pk>\d{1,8})/admin2$',
        AdministerRegistrationsView.as_view(),
        name='event_admin'),

    url(r'^(?P<pk>\d{1,8})/attendance$',
        RegisterAttendanceView.as_view(),
        name='event_register_attendance'),

    url(r'^$',
        calendar,
        name='event_list'),

    url(r'^(\d{4})/(\d{1,2})/$',
        calendar,
        name='event_list'),

    url(r'^fremover/$', EventMainPage.as_view(), name="event_main_page"),

    url(r'^mine/$',
        UserEventView.as_view(),
        name="view_user_events"),

    url(r'^(?P<pk>\d{1,8})/registration$',
        RegisterUserView.as_view(),
        name='registration'),

    url(r'^(?P<pk>\d{1,8})-(?P<slug>[-\w]*)$',
        EventDetailView.as_view(),
        name='event_detail'),

    url(r'^reg/(?P<pk>\d{1,8})$',
        EventRegistrationsView.as_view(),
        name='event_registrations'),

    url(r'^(?P<event_id>\d{1,8}).ics$',
        ical_event,
        name="ical_event"),

    url(r'^feed/$',
        RecentEvents(),
        name="event_feed"),
]
