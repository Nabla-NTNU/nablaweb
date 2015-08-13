# -*- coding: utf-8 -*-
from django.contrib.flatpages.models import FlatPage

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import TemplateView
from .models import Podcast, Season, get_season_count


class SeasonView(TemplateView):
    model = Season
    template_name = "podcast/season.html"

    def get_context_data(self, **kwargs):
        data = super(SeasonView, self).get_context_data(**kwargs)

        try:
            if 'number' in kwargs:
                number = kwargs['number']
                season = Season.objects.get(number=number)
            else:
                season = Season.objects.order_by('-number')[0]

            data['season'] = season
            data['season_name'] = season.name()
            data['podcast_list'] = Podcast.objects.filter(season=season).order_by('-pub_date').exclude(is_clip=True)
            data['podcast_clips'] = Podcast.objects.filter(season=season).order_by('-pub_date').exclude(is_clip=False)

            data['next'] = season.get_next()
            data['season_count'] = get_season_count()
            data['previous'] = season.get_previous()
        except IndexError:
            pass

        try:
            data['info'] = FlatPage.objects.get(url="/skraattcast/")
        except FlatPage.DoesNotExist:
            pass

        return data


def detail(request, podcast_id):
    current_podcast = Podcast.objects.get(id=podcast_id)
    current_podcast.add_view()
    template = loader.get_template('podcast/podcast_detail.html')
    context = RequestContext(request, {'podcast': current_podcast})

    context['season'] = season = current_podcast.season
    context['season_name'] = season.name()
    context['podcast_clips'] = Podcast.objects.filter(season=season).order_by('-pub_date').exclude(is_clip=False)

    return HttpResponse(template.render(context))
