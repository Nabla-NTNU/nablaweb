# -*- coding: utf-8 -*-
# nyheter/views.py

from nyheter.models import News
from nyheter.forms import NewsForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
import datetime

def show_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    return render_to_response('nyheter/base_news.html', {'content': news}, context_instance=RequestContext(request))

def list_news(request):
    news_list = News.objects.all()
    return render_to_response('nyheter/list_news.html', {'content_list': news_list}, context_instance=RequestContext(request))

def create_or_edit_news(request, news_id=None):
    if news_id is None:
        news = News()
    else:
        news = get_object_or_404(News, id=news_id)
    if request.method != 'POST':
        form = NewsForm(instance=news)
    else:
        form = NewsForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            news.headline = cd['headline']
            news.lead_paragraph = cd['lead_paragraph']
            news.body = cd['body']
            if news_id is None:
                news.created_by = request.user
            else:
                news.last_changed_by = request.user
            news.save()
            return HttpResponseRedirect(reverse('nyheter.views.show_news', args=(news.id,)))
    return render_to_response('nyheter/create_news.html', {'form': form}, context_instance=RequestContext(request))

def delete_news(request, news_id):
    return HttpResponse("Not yet implemented.")
