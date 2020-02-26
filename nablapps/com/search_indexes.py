from haystack import indexes

from .models import ComPage


class ComIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="com__name")
    description = indexes.CharField(model_attr="description")

    def get_model(self):
        return ComPage
