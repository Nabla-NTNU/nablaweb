# -*- coding: utf-8 -*-


from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, DeleteView
from content.models import Content
from news.models import News
from events.models import Event

from itertools import chain


class ContentListView(ListView):
    model = Content
    context_object_name = 'content_list'
    template_name = "content/content_list.html"
    paginate_by = 5

    def get_queryset(self):
        events = list(Event.objects.all().order_by('-created_date'))
        news = list(News.objects.all().order_by('-created_date'))

        queryset = sorted(chain(events, news), key=lambda content: content.created_date, reverse=True)

        return queryset


class ContentDetailView(DetailView):
    model = Content
    context_object_name = 'content'


class ContentDeleteView(DeleteView):
    model = Content
    context_object_name = 'content'

    def get_success_url(self):
        return reverse("%s_list" % self.model._meta.object_name.lower())
