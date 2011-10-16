from django.shortcuts import render

from events.models import Event
from news.models import News

from itertools import chain

def start(request):
    """Viser events og nyheter i samme liste"""
    events = Event.objects.all().order_by('-created_date')[:5]
    news = News.objects.all().order_by('-created_date')[:5]
    content_list = sorted(chain(events, news), key=lambda content: content.created_date, reverse=True)[:10]
    return render(request, 'homepage/homepage_start.html', {'content_list': content_list })

