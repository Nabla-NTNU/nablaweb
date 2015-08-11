# -*- coding: utf-8 -*-
from django.contrib.flatpages.models import FlatPage

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import ListView
from .models import Podcast, Season


class PodcastIndexView(ListView):
    model = Season
    paginate_by = 1
    queryset = Season.objects.order_by('-number')
    template_name = "podcast/podcast_list.html"

    def get_context_data(self, **kwargs):
        data = super(PodcastIndexView, self).get_context_data(**kwargs)
        season_list = data['season_list']
        try:
            data['season'] = season = season_list[0]
            data['season_name'] = "Sesong " + str(season.number)
            data['podcast_list'] = Podcast.objects.filter(season=season).order_by('-pub_date').exclude(is_clip=True)
            data['podcast_clips'] = Podcast.objects.filter(season=season).order_by('-pub_date').exclude(is_clip=False)
        except IndexError:
            pass

        try:
            data['info'] = FlatPage.objects.get(url="/scrattcast/")
        except FlatPage.DoesNotExist:
            pass

        return data


def detail(request, podcast_id):
    current_podcast = Podcast.objects.get(id=podcast_id)
    current_podcast.addView()
    template = loader.get_template('podcast/podcast_detail.html')
    context = RequestContext(request, {'podcast': current_podcast})
    return HttpResponse(template.render(context))
