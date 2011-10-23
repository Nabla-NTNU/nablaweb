from django.shortcuts import render
from quotes.models import Quote

def random_quote(request):
    try:
        quote = Quote.objects.order_by('?')[0]
    except:
        quote = ""
    return {'random_quote': quote }
