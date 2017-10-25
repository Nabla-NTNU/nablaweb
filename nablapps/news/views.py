from django.views.generic import DetailView, ListView
from content.views import AdminLinksMixin, ViewAddMixin, PublishedListMixin, PublishedMixin
from .models import NewsArticle


class NewsListView(PublishedListMixin, ListView):
    model = NewsArticle
    context_object_name = 'news_list'
    template_name = 'news/news_list.html'
    paginate_by = 8
    queryset = NewsArticle.objects.order_by('-pk')


class NewsDetailView(PublishedMixin, ViewAddMixin, AdminLinksMixin, DetailView):
    model = NewsArticle
    context_object_name = 'news'
    template_name = 'news/news_detail.html'
