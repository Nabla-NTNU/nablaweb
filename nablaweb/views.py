from django.views.generic import ListView
from content.models import Event
from bedpres.models import BedPres
from itertools import chain
from operator import attrgetter
from datetime import datetime, timedelta
from content.models.news import News
from content.views.mixins import PublishedListMixin
from podcast.models import Podcast
from nabladet.models import Nablad
from utils.view_mixins import FlatPageMixin


class FrontPageView(PublishedListMixin, FlatPageMixin, ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'front_page.html'
    paginate_by = 6
    queryset = News.objects.select_related('content_type').exclude(priority=0, published=False).order_by('-created_date')
    flatpages = [("sidebarinfo", "/forsideinfo/")]

    def get_context_data(self, **kwargs):
        context = super(FrontPageView, self).get_context_data(**kwargs)

        try:
            context['new_podcast'] = Podcast.objects.exclude(published=False)\
                .filter(is_clip=False).order_by('-pub_date')[0]
            context['new_nablad'] = Nablad.objects.exclude(published=False)\
                .order_by('-pub_date')[:3]
        except IndexError:
            pass

        now = datetime.now() - timedelta(hours=6)
        upcoming_events = Event.objects.filter(event_start__gte=now).order_by('event_start')[:6]
        upcoming_bedpreses = BedPres.objects.filter(event_start__gte=now).order_by('event_start')[:6]
        context['upcoming'] = sorted(chain(upcoming_events, upcoming_bedpreses), key=attrgetter("event_start"))[:6]

        return context
