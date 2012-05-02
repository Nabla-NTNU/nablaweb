# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from jobs.models import Advert

class RecentJobs(Feed):
    title = "Stillingsannonser på Nabla.no"
    link = "/stillinger"
    
    def items(self):
        return Advert.objects.order_by('-created_date')[:10]
        
    def item_title(self, item):
        return item.headline + " hos " + item.company.name
    
    def item_description(self, item):
        return item.lead_paragraph
