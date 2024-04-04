"""
Search index for NewsArticle

used by haystack
"""

from haystack import indexes

from .models import NewsArticle


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    """Search index for NewsArticle"""

    text = indexes.CharField(document=True, use_template=True)
    created_date = indexes.DateTimeField(model_attr="created_date")

    def get_model(self):
        return NewsArticle

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
