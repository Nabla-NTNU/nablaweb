# -*- coding: utf-8 -*-

from django.views.generic import ListView
from news.views import NewsDetailView
from meeting_records.models import MeetingRecord


class MeetingRecordDetailView(NewsDetailView):
    model = MeetingRecord
    context_object_name = 'meeting_record'
    template_name = "meeting_records/meeting_record_detail.html"

    def get_context_data(self, **kwargs):
        context = super(MeetingRecordDetailView, self).get_context_data(**kwargs)
        context['meeting_record_list'] = MeetingRecord.objects.order_by('-pub_date')
        return context


class MeetingRecordListView(ListView):
    model = MeetingRecord
    context_object_name = 'meeting_record_list'
    template_name = "meeting_records/meeting_record_list.html"

    def get_context_data(self, **kwargs):
        context = super(MeetingRecordListView, self).get_context_data(**kwargs)
        context['meeting_record_list'] = MeetingRecord.objects.order_by('-pub_date')
        return context
