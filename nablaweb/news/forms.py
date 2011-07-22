from nablaweb.content.forms import SiteContentForm, SiteContentFormPreview
from nablaweb.news.models import News


class NewsForm(SiteContentForm):
    class Meta(SiteContentForm.Meta):
        model = News

class NewsFormPreview(SiteContentFormPreview):
    form_template = 'news/news_form.html'
    preview_template = 'news/news_preview.html'
    form_base = 'news/news_form_base.html'
    success_detail = 'news_detail'
