from django.views.generic import TemplateView
from content.models import Event
from bedpres.models import BedPres
from datetime import datetime, timedelta
from content.models.news import News
from content.views.mixins import PublishedListMixin
from podcast.models import Podcast
from nabladet.models import Nablad
from utils.view_mixins import FlatPageMixin


class FrontPageView(PublishedListMixin, FlatPageMixin, TemplateView):
    model = News
    context_object_name = 'news_list'
    template_name = 'front_page.html'
    flatpages = [("sidebarinfo", "/forsideinfo/")]

    def get_context_data(self, **kwargs):
        context = super(FrontPageView, self).get_context_data(**kwargs)

        try:
            context['new_podcast'] = Podcast.objects.exclude(published=False)\
                .filter(is_clip=False).order_by('-pub_date')[0]
            context['main_news'] = News.objects.exclude(priority=0, published=False).order_by('-created_date')[0]
            context['news_list_1'] = News.objects.exclude(priority=0, published=False).order_by('-created_date')[1:3]
            context['news_list_2'] = News.objects.exclude(priority=0, published=False).order_by('-created_date')[3:5]
            context['news_list_3'] = News.objects.exclude(priority=0, published=False).order_by('-created_date')[5:7]
        except IndexError:
            pass

        context['new_nablad'] = Nablad.objects.exclude(published=False).order_by('-pub_date')[:4]

        now = datetime.now() - timedelta(hours=6)
        context['upcoming_events'] = Event.objects.filter(event_start__gte=now).order_by('event_start')[:6]
        context['upcoming_bedpreses'] = BedPres.objects.filter(event_start__gte=now).order_by('event_start')[:6]

        return context
