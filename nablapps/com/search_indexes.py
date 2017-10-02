from haystack import indexes
from .models import ComPage


class ComIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(model_attr='com__name')
    description = indexes.CharField(model_attr='description')
    last_changed_date = indexes.DateTimeField(model_attr='last_changed_date')
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ComPage
