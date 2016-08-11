from django.views.generic import TemplateView
from content.models import Event
from bedpres.models import BedPres
from datetime import datetime, timedelta
from content.models.news import News
from content.models import Album
from content.views.mixins import PublishedListMixin
from podcast.models import Podcast
from nabladet.models import Nablad
from utils.view_mixins import FlatPageMixin
from poll.models import Poll
from itertools import chain


class FrontPageView(PublishedListMixin, FlatPageMixin, TemplateView):
    model = News
    context_object_name = 'news_list'
    template_name = 'front_page.html'
    flatpages = [("sidebarinfo", "/forsideinfo/")]

    def get_context_data(self, **kwargs):
        context = super(FrontPageView, self).get_context_data(**kwargs)

        context['new_podcast'] = Podcast.objects.exclude(published=False).exclude(is_clip=True).first()
        news_list = News.objects.exclude(priority=0).exclude(published=False).order_by('-created_date')
        context['main_news'] = news_list.first()
        context['news_list_1'] = news_list[1:3]
        context['news_list_2'] = news_list[3:5]
        context['news_list_3'] = news_list[5:7]
        context['album_list'] = Album.objects.exclude(visibility='h').order_by('-last_changed_date')[:4]

        context['new_nablad'] = Nablad.objects.exclude(published=False).order_by('-pub_date')[:4]
        if not self.request.user.is_authenticated():
            context['new_nablad'] = Nablad.objects.exclude(published=False).exclude(is_public=False).order_by('-pub_date')[:4]

        now = datetime.now() - timedelta(hours=6)
        context['upcoming_events'] = Event.objects.filter(event_start__gte=now).exclude(organizer='BN').order_by('event_start')[:6]
        # denne løsningen er litt stygg, men jeg tror det er den letteste
        bedpresArr = Event.objects.filter(event_start__gte=now, organizer='BN')
        bedpres = BedPres.objects.filter(event_start__gte=now)
        context['upcoming_bedpreses'] = sorted(chain(bedpresArr, bedpres), key=lambda x: x.event_start)[:6]
        context['poll'] = Poll.objects.exclude(is_user_poll=True).order_by('-publication_date').first()
        if self.request.user.is_authenticated() and context['poll'] is not None:
            context['poll_has_voted'] = context['poll'].user_has_voted(self.request.user)
        return context
