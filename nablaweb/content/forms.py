from django.forms import ModelForm
from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from nablaweb.content.models import SiteContent
from django.shortcuts import get_object_or_404

class SiteContentForm(ModelForm):
    class Meta:
        model = SiteContent


class SiteContentFormPreview(FormPreview):
    form_template = 'content/content_form.html'
    preview_template = 'content/content_preview.html'
    form_base = 'content/content_form_base.html'

    def done(self, request, cleaned_data, Model=SiteContent, success_view='content_detail'):
        content = Model(**cleaned_data)
        content.created_by = request.user
        content.save()
        return HttpResponseRedirect(reverse(success_view, args=(content.id,)))

    def process_preview(self, request, form, context):
        content = form.save(commit=False)
        content.created_by = request.user
        context['content'] = content

    def get_context(self, request, form):
        context = super(SiteContentFormPreview, self).get_context(request, form)
        context['form_base'] = self.form_base
        return context
