# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView, ListView
from django.shortcuts import redirect

from ..templatetags import listutil
from ..models.news import News
from .mixins import AdminLinksMixin, ViewAddMixin, PublishedListMixin, PublishedMixin


class WrongContentType(Exception):
    def __init__(self, object):
        self.object = object


class NewsListView(PublishedListMixin, ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'content/news/news_list.html'
    paginate_by = 8
    queryset = News.objects.select_related('content_type').exclude(priority=0).order_by('-pk')


class NewsDetailView(PublishedMixin, ViewAddMixin, AdminLinksMixin, DetailView):
    model = News
    context_object_name = 'news'
    template_name = 'content/news/news_detail.html'

    def get_object(self):
        object = super().get_object()
        if object.content_type != ContentType.objects.get_for_model(self.model):
            raise WrongContentType(object)
        return object

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except WrongContentType as e:
            return redirect(e.object)
