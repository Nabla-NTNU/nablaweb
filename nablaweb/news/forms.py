from nablaweb.content.forms import ContentForm, ContentFormPreview
from nablaweb.news.models import News


class NewsForm(ContentForm):
    class Meta(ContentForm.Meta):
        model = News

class NewsFormPreview(ContentFormPreview):
    form_template = 'news/news_form.html'
    preview_template = 'news/news_preview.html'
    form_base = 'news/news_form_base.html'
    success_detail = 'news_detail'
