# nyheter/forms.py

from innhold.forms import SiteContentForm
from nyheter.models import News

class NewsForm(SiteContentForm):
    class Meta(SiteContentForm.Meta):
        model = News
