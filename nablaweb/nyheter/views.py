from nyheter.models import News
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def show_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    return render_to_response('nyheter/base_news.html', {'content': news}, context_instance=RequestContext(request))
