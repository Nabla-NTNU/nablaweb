from haystack import indexes
from .models import Podcast


class PodcastIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Podcast
