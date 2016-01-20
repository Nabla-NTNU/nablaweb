from django.views.generic import ListView


from content.templatetags import listutil
from content.models.news import News
from content.views.mixins import PublishedListMixin
from podcast.models import Podcast
from poll.context_processors import poll_context
from .context_processors import upcoming_events
from utils.view_mixins import FlatPageMixin


class FrontPageView(PublishedListMixin, FlatPageMixin, ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'front_page.html'
    paginate_by = 7
    queryset = News.objects.select_related('content_type').exclude(priority=0, published=False).order_by('-pk')
    flatpages = [("sidebarinfo", "/forsideinfo/")]

    def get_context_data(self, **kwargs):
        """
        Deler innholdet opp i en featured_news og rader med to nyheter hver,
        news_rows = [[n1, n2], [n3, n4]] etc.
        """

        context = super(FrontPageView, self).get_context_data(**kwargs)

        try:
            context['new_podcast'] = Podcast.objects.exclude(published=False).filter(is_clip=False).order_by('-pub_date')[0]
        except IndexError:
            pass

        context.update(upcoming_events(self.request))
        context.update(poll_context(self.request))

        return context
