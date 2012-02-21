# -*- coding: utf-8 -*-

# Views for quotes-appen

from quotes.models import Quote
from django.views.generic import ListView, RedirectView
from django.shortcuts import get_object_or_404, get_list_or_404

class ListAllQuotes(ListView):
    model = Quote
    context_object_name = "content_list"
    paginate_by = 10

    template_name = "quotes/quotes_list.html"
    
    @staticmethod
    def active_jobs(request):
        quotes = Quote.objects.filter()
        return {'quotes': quotes}
    
    def get_queryset(self):
        return Quote.objects.filter()
