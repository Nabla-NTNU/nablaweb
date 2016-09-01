from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import University, Exchange, Info
from django.db.models import Q


class ExchangeListView(ListView):
    model = University
    template_name = "exchange/ex_list.html"
    context_object_name = "ex_list"

    def get_queryset(self):
        query = self.request.GET.get("q")
        ex_list = University.objects.all()
        if query:
            ex_list = University.objects.filter(Q(land__icontains=query)|Q(univ_navn__icontains=query))
        return ex_list


class ExDetailListView(DetailView):
    template_name = "exchange/ex_detail_list.html"
    model = University

    def get_context_data(self, **kwargs):
        context = super(ExDetailListView, self).get_context_data(**kwargs)
        context['link_list'] = Info.objects.filter(ex__univ=self.object)
        context['ex_detail_list'] = Exchange.objects.filter(univ=self.object)
        context['url'] = '/utveksling/' + str(self.object.pk) + '/'
        return context
