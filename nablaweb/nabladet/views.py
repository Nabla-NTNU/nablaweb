# -*- coding: utf-8 -*-

from news.views import NewsListView, NewsDetailView, NewsDeleteView
from nabladet.models import Nablad

class NabladDetailView(NewsDetailView):
    model = Nablad
    context_object_name = 'nablad'

class NabladListView(NewsListView):
    model = Nablad
    context_object_name = 'nablad_list'

