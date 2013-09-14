# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from meeting_records.views import MeetingRecordListView, MeetingRecordDetailView

urlpatterns = patterns('meeting_records.views',
    # Offentlig
    url(r'^$', 
        MeetingRecordListView.as_view( context_object_name = "meeting_record_list" ),
        name='nablad_list'),
    url(r'^(?P<pk>\d{1,8})/(?P<slug>[-\w]*)$', 
        MeetingRecordDetailView.as_view( context_object_name = "meeting_record" ),
        name='nablad_detail'),
)
