from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Universitet, Utveksling, Link
from django.db.models import Q





class ExchangeListView(ListView):
    model = Universitet
    template_name = "exchange/ex_list.html"
    context_object_name = "ex_list"
    def get_queryset(self):
        query = self.request.GET.get("q")
        ex_list = Universitet.objects.all()
        if query:
            ex_list = Universitet.objects.filter(Q(land__icontains=query)|Q(univ_navn__icontains=query))
        return ex_list


class ExDetailListView(ListView):
    template_name="exchange/ex_detail_list.html"
    context_object_name = "ex_detail_list"
    queryset = Utveksling.objects.all()


    def get_context_data(self, **kwargs):
        context = super(ExDetailListView, self).get_context_data(**kwargs)
        context['link_list'] = Link.objects.all()
        context['ex_list'] = Universitet.objects.all()



        return context