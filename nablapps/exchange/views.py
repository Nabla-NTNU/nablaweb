from django.views.generic import ListView, DetailView, TemplateView
from .models import University, Exchange, Info, RETNINGER, ExchangeNewsArticle
from django.db.models import Q

from django.urls import reverse

class ExchangeFrontpageView(TemplateView):
    template_name = 'exchange/exchange_frontpage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exchange_news_query = ExchangeNewsArticle.objects.all()
        exchange_news = []
        for news in exchange_news_query[len(exchange_news_query)-3:]:
            exchange_news.insert(0, news)
        ex_list_url = reverse('ex_list')
        ex_news_url = reverse('ex_news')
        context['news_list'] = exchange_news
        context['ex_list_url'] = ex_list_url
        context['ex_news_url'] = ex_news_url
        return context


class ExchangeNewsView(ListView):
    template_name = 'exchange/exchange_news.html'
    model = ExchangeNewsArticle
    context_object_name = 'news_list'
    paginate_by = 8 
    queryset = ExchangeNewsArticle.objects.order_by('-pk')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ex_frontpage_url = reverse('ex_frontpage')
        ex_list_url = reverse('ex_list')
        context['ex_frontpage_url'] = ex_frontpage_url
        context['ex_list_url'] = ex_list_url
        return context


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
        ex_frontpage_url = reverse('ex_frontpage')
        context['ex_frontpage_url'] = ex_frontpage_url
        context['retninger'] = [long_name.capitalize() for _, long_name in RETNINGER]
        return context


class UnivDetailView(DetailView):
    template_name = "exchange/ex_detail_list.html"
    model = University

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info'] = Info.objects.filter(ex__univ=self.object)
        context['ex_detail_list'] = Exchange.objects.filter(univ=self.object)\
                                                    .select_related("student")
        return context


class InfoDetailView(DetailView):
    template_name = "exchange/info.html"
    model = Info
