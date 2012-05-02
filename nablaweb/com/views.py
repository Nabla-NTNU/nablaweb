# -*- coding: utf-8 -*-

# Views for com-appen

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import DetailView, ListView
from django.template.defaultfilters import slugify
from com.models import ComPage, ComMembership

class ShowPage(DetailView):
    template_name = 'com/com_details.html'
    model = ComPage
    context_object_name = 'com'
    
    def canonical_name(self):
        return slugify(self.kwargs['slug'])
    
    def get_context_data(self, **kwargs):
        context = super(ShowPage, self).get_context_data(**kwargs)
        c = self.get_object()
        context['members'] = ComMembership.objects.filter(com = c)
        return context
