# -*- coding: utf-8 -*-

from django.views.generic import DetailView, ListView

from ..templatetags import listutil
from ..models.news import News
from .mixins import AdminLinksMixin, ViewAddMixin, PublishedListMixin, PublishedMixin


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
