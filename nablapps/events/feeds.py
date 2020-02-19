"""
Feed for events
"""
from django.contrib.syndication.views import Feed

from .models import Event


class RecentEvents(Feed):
    """Feed class for Event-model"""

    title = "Arrangement på Nabla.no"
    link = "/arrangement"

    def items(self):
        """Return queryset of events"""
        return Event.objects.order_by("-created_date")[:10]

    def item_title(self, item):
        return item.headline

    def item_description(self, item):
        return item.lead_paragraph
