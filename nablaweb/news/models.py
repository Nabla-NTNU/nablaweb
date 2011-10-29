from content.models import Content

class News(Content):
    class Meta(Content.Meta):
        verbose_name = "nyhet"
        verbose_name_plural = "nyheter"
