from django.contrib.syndication.views import Feed
from .models import Event


class RecentEvents(Feed):
    title = "Arrangement på Nabla.no"
    link = "/arrangement"

    def items(self):
        return Event.objects.order_by('-created_date')[:10]

    def item_title(self, item):
        return item.headline

    def item_description(self, item):
        return item.lead_paragraph
