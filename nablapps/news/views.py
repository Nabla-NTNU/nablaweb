"""
Views for the news app
"""
from django.views.generic import DetailView, ListView
from nablapps.core.view_mixins import AdminLinksMixin
from .models import NewsArticle


class NewsListView(ListView):
    """List of news-articles"""
    model = NewsArticle
    context_object_name = 'news_list'
    template_name = 'news/news_list.html'
    paginate_by = 8
    queryset = NewsArticle.objects.order_by('-pk')


class NewsDetailView(AdminLinksMixin, DetailView):
    """Show a single news-article"""
    model = NewsArticle
    context_object_name = 'news'
    template_name = 'news/news_detail.html'
