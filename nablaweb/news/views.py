# -*- coding: utf-8 -*-


from news.models import News
from news.forms import NewsForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
import datetime


def create_or_edit_news(request, news_id=None):
    # Sjekk om nyheten skal endres; ingen news_id betyr ny nyhet.
    if news_id is None:
        news = News()
    else:
        news = get_object_or_404(News, id=news_id)
    if request.method != 'POST':
        form = NewsForm(instance=news)
    else:
        form = NewsForm(data=request.POST, instance=news)
        if form.is_valid():
            news = form.save(commit=False)
            if news_id is None:
                news.created_by = request.user
            else:
                news.last_changed_by = request.user
            news.save()
            return HttpResponseRedirect(reverse('news.views.show_news', args=(news.id,)))
    return render_to_response('news/news_create.html', {'form': form}, context_instance=RequestContext(request))
