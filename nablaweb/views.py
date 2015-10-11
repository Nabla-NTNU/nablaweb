from django.views.generic import ListView

from content.templatetags import listutil
from content.models.news import News
from podcast.models import Podcast
from poll.context_processors import poll_context
from .context_processors import upcoming_events


class FrontPageView(ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'front_page.html'
    paginate_by = 7  # Oddetall ser finest ut
    queryset = News.objects.select_related('content_type').exclude(priority=0).order_by('-pk')

    def get_context_data(self, **kwargs):
        """
        Deler innholdet opp i en featured_news og rader med to nyheter hver,
        news_rows = [[n1, n2], [n3, n4]] etc.
        """
        context = super(FrontPageView, self).get_context_data(**kwargs)

        from django.contrib.flatpages.models import FlatPage
        try:
            context['sidebarinfo'] = FlatPage.objects.get(url="/forsideinfo/")
            context['new_podcast'] = Podcast.objects.filter(is_clip=False).order_by('-pub_date')[0]
        except FlatPage.DoesNotExist:
            pass

        news_list = context['news_list']

        if news_list:
            context['featured_news'] = news_list[0]

            # Deler f.eks. opp [1, 2, 3, 4, 5] til [[1, 2], [3, 4], [5]]
            context['news_rows'] = listutil.row_split(news_list[1:], 2)

        context.update(upcoming_events(self.request))
        context.update(poll_context(self.request))

        return context
