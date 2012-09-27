# -*- coding: utf-8 -*-

from django.views.generic import ListView
from news.views import NewsDetailView
from nabladet.models import Nablad


class NabladDetailView(NewsDetailView):
    model = Nablad
    context_object_name = 'nablad'

    def get_context_data(self, **kwargs):
        context = super(NabladDetailView, self).get_context_data(**kwargs)
        nablad_list = Nablad.objects.all()
        context['nablad_list'] = Nablad.objects.all()
        return context


class NabladListView(ListView):
    model = Nablad
    context_object_name = 'nablad_list'
    queryset = Nablad.objects.all()
