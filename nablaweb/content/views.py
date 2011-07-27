# -*- coding: utf-8 -*-


from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, DeleteView
from nablaweb.content.models import SiteContent
from nablaweb.news.models import News


class SiteContentListView(ListView):
    model = SiteContent
    context_object_name = 'content_list'
    paginate_by = 5

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-created_date')
        return queryset


class SiteContentDetailView(DetailView):
    model = SiteContent
    context_object_name = 'content'


class SiteContentDeleteView(DeleteView):
    model = SiteContent
    context_object_name = 'content'
    
    def get_success_url(self):
        return reverse("%s_list" % self.model._meta.object_name.lower())
