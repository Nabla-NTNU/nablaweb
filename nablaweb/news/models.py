from content.models import Content

class News(Content):
    class Meta(Content.Meta):
        verbose_name_plural = "news"
