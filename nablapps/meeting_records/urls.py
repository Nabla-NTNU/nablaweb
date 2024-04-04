"""
Urls for meeting_records app
"""

from django.urls import path

from .views import MeetingRecordDetailView, MeetingRecordListView

urlpatterns = [
    path("<int:year>/", MeetingRecordListView.as_view(), name="meeting_record_list"),
    path(
        "<int:pk>/<str:slug>/",
        MeetingRecordDetailView.as_view(),
        name="meetingrecord_detail",
    ),
]
