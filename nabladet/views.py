# -*- coding: utf-8 -*-

from django.views.generic import ListView
from content.views import NewsDetailView
from nabladet.models import Nablad
from django.http import HttpResponseRedirect


class NabladDetailView(NewsDetailView):
    model = Nablad
    template_name = 'nabladet/nablad_detail.html'
    context_object_name = 'nablad'

    def get_context_data(self, **kwargs):
        context = super(NabladDetailView, self).get_context_data(**kwargs)
        context['nablad_archive'] = Nablad.objects.order_by('-pub_date')
        if not self.request.user.is_authenticated():
            context['nablad_archive'].exclude(is_public=False).order_by('-pub_date')
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or Nablad.objects.get(pk=kwargs['pk']).is_public :
            return HttpResponseRedirect('/login/')
        return super(NabladDetailView, self).dispatch(request, *args, **kwargs)


class NabladListView(ListView):
    model = Nablad
    template_name = "nabladet/nablad_list.html"
    context_object_name = "nablad_list"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated():
            queryset = queryset.exclude(is_public=False)
        return queryset
