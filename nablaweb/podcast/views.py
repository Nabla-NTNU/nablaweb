# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from podcast.models import Podcast

def index(request):
    latest_podcast_list = Podcast.objects.order_by('-pub_date')[:8]
    template = loader.get_template('podcast/podcast_list.html')
    context = RequestContext(request, {
        'latest_podcast_list': latest_podcast_list,
    })
    return HttpResponse(template.render(context))

def detail(request, podcast_id):
    current_podcast = Podcast.objects.get(id=podcast_id)
    template = loader.get_template('podcast/podcast_detail.html')
    context = RequestContext(request, {'podcast': current_podcast})
    return HttpResponse(template.render(context))
