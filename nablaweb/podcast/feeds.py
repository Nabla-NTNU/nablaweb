# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.models import Podcast

class LatestEntriesFeed(Feed):
    title: ''
    link: ''
    description = ''

    def item(self):
        return Podcast.objects.order_by('-pub_date')[:5]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.description
    def item_link(self, item):
        return reverse('podcast', args[item.pk])

