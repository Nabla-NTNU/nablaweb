"""
RSS feed for front page news
"""

from django.contrib.syndication.views import Feed

from .models import FrontPageNews


class RecentNews(Feed):
    """Feed showing the news on the front page"""

    title = "Nyheter på Nabla.no"
    link = "/"

    def items(self):  # pylint: disable=C0111
        return FrontPageNews.objects.order_by("-created_date")[:10]

    def item_title(self, item):
        return item.headline

    def item_description(self, item):
        return item.lead_paragraph
