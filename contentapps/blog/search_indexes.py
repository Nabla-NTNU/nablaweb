from haystack import indexes
from .models import BlogPost


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')
    created_date = indexes.DateTimeField(model_attr='created_date')
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return BlogPost
