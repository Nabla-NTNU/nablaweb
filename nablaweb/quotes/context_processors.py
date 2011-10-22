from django.shortcuts import render
from quotes.models import Quote

def random_quote(request):
    quote = Quote.objects.order_by('?')[0]
    return {'random_quote': quote }
