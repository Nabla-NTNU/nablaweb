from django.contrib.syndication.views import Feed
from .models import FrontPageNews


class RecentNews(Feed):
    title = "Nyheter på Nabla.no"
    link = "/"

    def items(self):
        return FrontPageNews.objects.order_by('-created_date')[:10]

    def item_title(self, item):
        return item.headline

    def item_description(self, item):
        return item.lead_paragraph
