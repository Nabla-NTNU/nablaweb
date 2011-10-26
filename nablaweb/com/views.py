# -*- coding: utf-8 -*-

# Views for com-appen

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import DetailView, ListView
from com.models import *

class ShowPage(DetailView):
    template_name = 'com/com_details.html'

    model = ComPage
    slug_field = 'com__group__name'
    context_object_name = 'com'
   
    def get_context_data(self, **kwargs):
        context = super(ShowPage, self).get_context_data(**kwargs)
        c = self.get_object()
        context['members'] = ComMember.objects.filter(com = c)

class ListComs(ListView):
    pass
