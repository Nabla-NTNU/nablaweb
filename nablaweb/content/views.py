# -*- coding: utf-8 -*-


from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from nablaweb.content.models import SiteContent
from nablaweb.content.forms import SiteContentForm


class ContentUpdateView(UpdateView):
    model = SiteContent
    form_class = SiteContentForm
    template_name = 'content/content_form.html'
    form_base = 'content/content_form_base.html'
    success_detail = 'content_detail'

    def get_success_url(self):
        return reverse(self.success_detail, args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context_data = super(ContentUpdateView, self).get_context_data(**kwargs)
        context_data['form_base'] = self.form_base
        return context_data
