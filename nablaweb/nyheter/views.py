# -*- coding: utf-8 -*-
# nyheter/views.py

from nyheter.models import News
from nyheter.forms import NewsForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
import datetime

def show_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    return render_to_response('nyheter/base_news.html', {'content': news}, context_instance=RequestContext(request))

def list_news(request):
    news_list = News.objects.all()[:10]
    return render_to_response('nyheter/list_news.html', {'content_list': news_list}, context_instance=RequestContext(request))

def create_news(request):
    return HttpResponse("Not yet implemented.")

def edit_news(request):
    return HttpResponse("Not yet implemented.")

def delete_news(request, news_id):
    return HttpResponse("Not yet implemented.")
