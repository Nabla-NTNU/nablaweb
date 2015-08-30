# -*- coding: utf-8 -*-

from django.conf.urls import *
from meeting_records.views import MeetingRecordListView, MeetingRecordDetailView

urlpatterns = patterns('meeting_records.views',
                       url(r'^$',
                           MeetingRecordListView.as_view(context_object_name="meeting_record_list"),
                           name='meeting_record_list'),
                       url(r'^(?P<pk>\d{1,8})/(?P<slug>[-\w]*)$',
                           MeetingRecordDetailView.as_view(context_object_name="meeting_record"),
                           name='meetingrecord_detail'),
                       )
