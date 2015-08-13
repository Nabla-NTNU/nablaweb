# -*- coding: utf-8 -*-

from django.views.generic import ListView
from content.views import NewsDetailView
from nabladet.models import Nablad


class NabladDetailView(NewsDetailView):
    model = Nablad
    context_object_name = 'nablad'

    def get_context_data(self, **kwargs):
        context = super(NabladDetailView, self).get_context_data(**kwargs)
        context['nablad_archive'] = Nablad.objects.order_by('-pub_date')
        return context


class NabladListView(ListView):
    model = Nablad
    context_object_name = "nablad_list"
