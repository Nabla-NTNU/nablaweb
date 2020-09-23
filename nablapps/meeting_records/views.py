"""
Views for meeting records
"""
from django.views.generic import DetailView, ListView
from django.views.generic.dates import YearArchiveView
from django.core.paginator import EmptyPage, Paginator

from .models import MeetingRecord


class MeetingRecordDetailView(DetailView):
    """
    View showing a single meeting record along with a list of other meeting records.
    """

    model = MeetingRecord
    context_object_name = "meeting_record"
    template_name = "meeting_records/meeting_record_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meeting_record_list"] = MeetingRecord.objects.order_by("-pub_date")
        return context


class MeetingRecordListView(YearArchiveView):
    """
    View listing all meeting records
    """

    queryset = MeetingRecord.objects.all()
    context_object_name = "meeting_record_list"
    template_name = "meeting_records/meeting_record_list.html"
    date_field = "pub_date"
    make_object_list = True
    allow_future = False
    allow_empty = False
