from nablaweb.content.forms import SiteContentForm, SiteContentFormPreview
from nablaweb.news.models import News


class NewsForm(SiteContentForm):
    class Meta(SiteContentForm.Meta):
        model = News


class NewsFormPreview(SiteContentFormPreview):
    form_template = 'news/news_form.html'
    preview_template = 'news/news_preview.html'

    def done(self, request, cleaned_data):
        return super(NewsFormPreview, self).done(request, cleaned_data, Model=News, success_view='news_detail')
