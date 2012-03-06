# -*- coding: utf-8 -*-

from django.views.generic import ListView
from news.views import NewsDetailView
from nabladet.models import Nablad


class NabladDetailView(NewsDetailView):
    model = Nablad
    context_object_name = 'nablad'


class NabladListView(ListView):
    model = Nablad
    context_object_name = 'nablad_list'
    queryset = Nablad.objects.all()
