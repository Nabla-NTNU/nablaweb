# -*- coding: utf-8 -*-

from contentapps.news.views import NewsDetailView
from django.contrib.auth.views import redirect_to_login
from django.views.generic import ListView

from nablapps.nabladet.models import Nablad


class NabladDetailView(NewsDetailView):
    model = Nablad
    template_name = 'nabladet/nablad_detail.html'
    context_object_name = 'nablad'

    def get_context_data(self, **kwargs):
        context = super(NabladDetailView, self).get_context_data(**kwargs)
        context['nablad_archive'] = Nablad.objects.order_by('-pub_date')
        if not self.request.user.is_authenticated():
            context['nablad_archive'] = context['nablad_archive'].exclude(is_public=False).order_by('-pub_date')
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            nablad = self.get_object()
            if not nablad.is_public:
                return redirect_to_login(next=nablad.get_absolute_url())
        return super().get(request, *args, **kwargs)


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
