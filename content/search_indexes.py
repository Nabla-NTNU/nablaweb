from haystack import indexes
from content.models.album import Album
from content.models.news import News
from content.models.blog import BlogPost


class AlbumIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='title')
    created_date = indexes.DateTimeField(model_attr='created_date')
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Album


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    headline = indexes.CharField(model_attr='headline')
    lead_paragraph = indexes.CharField(model_attr='lead_paragraph')
    body = indexes.CharField(model_attr='body')
    created_date = indexes.DateTimeField(model_attr='created_date')
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(published=False)


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')
    created_date = indexes.DateTimeField(model_attr='created_date')
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return BlogPost

