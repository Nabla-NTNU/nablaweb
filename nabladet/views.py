# -*- coding: utf-8 -*-

from django.views.generic import ListView
from content.views import NewsDetailView
from nabladet.models import Nablad
from braces.views import LoginRequiredMixin


class NabladDetailView(LoginRequiredMixin, NewsDetailView):
    model = Nablad
    template_name = 'nabladet/nablad_detail.html'
    context_object_name = 'nablad'

    def get_context_data(self, **kwargs):
        context = super(NabladDetailView, self).get_context_data(**kwargs)
        context['nablad_archive'] = Nablad.objects.order_by('-pub_date')
        return context


class NabladListView(LoginRequiredMixin, ListView):
    model = Nablad
    template_name = "nabladet/nablad_list.html"
    context_object_name = "nablad_list"
    paginate_by = 12
