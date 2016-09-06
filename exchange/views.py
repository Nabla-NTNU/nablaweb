from django.views.generic import ListView, DetailView
from .models import University, Exchange, Info, RETNINGER
from django.db.models import Q


class ExchangeListView(ListView):
    model = University
    template_name = "exchange/ex_list.html"
    context_object_name = "ex_list"

    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = University.objects.order_by('land')
        if query:
            queryset = queryset.filter(Q(land__icontains=query) | Q(univ_navn__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['retninger'] = [long_name.capitalize() for _, long_name in RETNINGER]
        return context


class UnivDetailView(DetailView):
    template_name = "exchange/ex_detail_list.html"
    model = University

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info'] = Info.objects.filter(ex__univ=self.object)
        context['ex_detail_list'] = Exchange.objects.filter(univ=self.object).select_related("student")
        
        return context


class InfoDetailView(DetailView):
    template_name = "exchange/info.html"
    model = Info
