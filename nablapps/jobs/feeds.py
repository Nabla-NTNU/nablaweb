"""
Rss feed for jobs
"""
from django.contrib.syndication.views import Feed
from nablapps.jobs.models import Advert


class RecentJobs(Feed):
    """Rss feed showing the most recent job adverts"""
    title = "Stillingsannonser på Nabla.no"
    link = "/stillinger"

    def items(self):
        """Get the adverts to show"""
        return Advert.objects.order_by('-created_date')[:10]

    def item_title(self, item):
        return f"{item.headline} hos {item.company.name}"

    def item_description(self, item):
        return item.lead_paragraph
