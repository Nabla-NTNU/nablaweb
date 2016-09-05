from django.views.generic import ListView, DetailView
from .models import University, Exchange, Info, RETNINGER
from django.db.models import Q


class ExchangeListView(ListView):
    model = University
    template_name = "exchange/ex_list.html"
    context_object_name = "ex_list"

    def get_queryset(self):
        query = self.request.GET.get("q")
        ex_list = University.objects.order_by('land')
        if query:
            ex_list = University.objects.filter(Q(land__icontains=query)|Q(univ_navn__icontains=query))
        return ex_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['retninger'] = [i[1].capitalize() for i in RETNINGER]
        for univ in context['ex_list']:
            univ.retninger = []
            for retn in RETNINGER:
                univ.retninger.append(Exchange.objects.filter(univ=univ).filter(retning=retn[0]).exists())
        return context


class UnivDetailView(DetailView):
    template_name = "exchange/ex_detail_list.html"
    model = University

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info'] = Info.objects.filter(ex__univ=self.object)
        context['ex_detail_list'] = Exchange.objects.filter(univ=self.object)
        for obj in context['ex_detail_list']:
            obj.name = obj.student.get_full_name()
            obj.mail = obj.student.email
        return context


class InfoDetailView(DetailView):
    template_name = "exchange/info.html"
    model = Info

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['univ'] = self.object.ex.univ
        return context
