"""
Urls for events
"""
from django.urls import path, re_path

from .feeds import RecentEvents
from .views import (
    AdministerRegistrationsView,
    EventDetailView,
    EventMainPage,
    EventRegistrationsView,
    RegisterAttendanceView,
    RegisterUserView,
    UserEventView,
    calendar,
    ical_event,
)

urlpatterns = [
    path(
        "<int:pk>/admin2/", AdministerRegistrationsView.as_view(), name="event_admin",
    ),
    path(
        "<int:pk>/attendance/",
        RegisterAttendanceView.as_view(),
        name="event_register_attendance",
    ),
    path("", EventMainPage.as_view(), name="event_main_page"),
    path("calendar/", calendar, name="event_list"),
    re_path(r"^calendar/(\d{4})/(\d{1,2})/$", calendar, name="event_list"),
    path("mine/", UserEventView.as_view(), name="view_user_events"),
    path("<int:pk>/registration/", RegisterUserView.as_view(), name="registration",),
    re_path(
        r"^(?P<pk>\d{1,8})-(?P<slug>[-\w]*)$",
        EventDetailView.as_view(),
        name="event_detail",
    ),
    path(
        "reg/<int:pk>/", EventRegistrationsView.as_view(), name="event_registrations",
    ),
    re_path(r"^(?P<event_id>\d{1,8}).ics$", ical_event, name="ical_event"),
    path("feed/", RecentEvents(), name="event_feed"),
]
