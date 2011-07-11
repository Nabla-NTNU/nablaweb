from content.forms import SiteContentForm
from news.models import News

class NewsForm(SiteContentForm):
    class Meta(SiteContentForm.Meta):
        model = News
