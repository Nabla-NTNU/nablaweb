# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed

from content.models.events import Event


class RecentEvents(Feed):
    title = "Arrangement på Nabla.no"
    link = "/arrangement"
    
    def items(self):
        return Event.objects.order_by('-created_date')[:10]
        
    def item_title(self, item):
        return item.headline
    
    def item_description(self, item):
        return item.lead_paragraph
