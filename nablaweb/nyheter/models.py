# nyheter/models.py

from innhold.models import SiteContent

class News(SiteContent):
    class Meta(SiteContent.Meta):
        verbose_name_plural = "news"
