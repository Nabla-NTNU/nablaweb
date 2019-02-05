"""
Core views in nablaweb
"""
from datetime import datetime, timedelta
from itertools import chain

from django.views.generic import TemplateView

from nablapps.album.models import Album
from nablapps.blog.models import BlogPost

from ..bedpres.models import BedPres
from ..events.models import Event
from ..nabladet.models import Nablad
from ..news.models import FrontPageNews
from ..podcast.models import Podcast
from ..poll.models import Poll
from .view_mixins import FlatPageMixin


class FrontPageView(FlatPageMixin, TemplateView):
    """
    The view for showing the front page of nablaweb
    """
    template_name = 'front_page.html'
    flatpages = [("sidebarinfo", "/forsideinfo/")]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Inject complicated context.
        # This context processing should perhaps be moved to the corresponding apps.
        self._add_news(context)
        self._add_events_and_bedpres(context)
        self._add_poll(context)
        self._add_nablad(context)
        context['new_podcast'] = Podcast.objects.exclude(is_clip=True).first()
        context['album_list'] = Album.objects.exclude(visibility='h').order_by('-last_changed_date')[:4]
        context['new_blog'] = BlogPost.objects.exclude(list_image=None).order_by('-created_date')[:4]
        return context

    def _add_news(self, context):
        news_list = FrontPageNews.objects.filter(visible=True)
        context['main_news'] = news_list.first()
        context['news_list_1'] = news_list[1:3]
        context['news_list_2'] = news_list[3:5]
        context['news_list_3'] = news_list[5:7]

    def _add_nablad(self, context):
        context['new_nablad'] = Nablad.objects.order_by('-pub_date')[:4]
        if not self.request.user.is_authenticated:
            context['new_nablad'] = Nablad.objects.exclude(is_public=False).order_by('-pub_date')[:4]

    def _add_events_and_bedpres(self, context):
        now = datetime.now() - timedelta(hours=6)
        context['upcoming_events'] = Event.objects.filter(event_start__gte=now).exclude(organizer='BN').order_by('event_start')[:6]
        # denne løsningen er litt stygg, men jeg tror det er den letteste
        bedpresArr = Event.objects.filter(event_start__gte=now, organizer='BN')
        bedpres = BedPres.objects.filter(event_start__gte=now)
        context['upcoming_bedpreses'] = sorted(chain(bedpresArr, bedpres), key=lambda x: x.event_start)[:6]

    def _add_poll(self, context):
        try:
            context['poll'] = Poll.objects.current_poll()
        except:
            context['poll'] = Poll.objects.exclude(is_user_poll=True).order_by('-publication_date').first()

        if self.request.user.is_authenticated and context['poll'] is not None:
            context['poll_has_voted'] = context['poll'].user_has_voted(self.request.user)
