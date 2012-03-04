# -*- coding: utf-8 -*-


from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, DeleteView
from news.models import News


class NewsListView(ListView):
    model = News
    context_object_name = 'news_list'
    paginate_by = 7
    queryset = News.objects.all().select_subclasses()


class NewsDetailView(DetailView):
    model = News
    context_object_name = 'news'


class NewsDeleteView(DeleteView):
    model = News
    context_object_name = 'news'

    def get_success_url(self):
        return reverse("%s_list" % self.model._meta.object_name.lower())
