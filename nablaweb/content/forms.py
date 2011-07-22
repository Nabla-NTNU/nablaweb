# -*- coding: utf-8 -*-


import datetime
from django.forms import ModelForm
from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from nablaweb.content.models import SiteContent


class SiteContentForm(ModelForm):
    class Meta:
        model = SiteContent


class UpdateableModelFormPreview(FormPreview):
    def preview_get(self, request):
        "Displays the form"
        f = self.form(auto_id=self.get_auto_id(), instance=self.get_instance(),  initial=self.get_initial(request))
        return render_to_response(self.form_template,
            self.get_context(request, f),
            context_instance=RequestContext(request))

    def get_instance(self):
        return self.state.get('instance')

    def is_updating(self):
        return bool(self.get_instance())

    def get_model(self):
        return self.form.Meta.model

    def parse_params(self, *args, **kwargs):
        super(UpdateableModelFormPreview, self).parse_params(*args, **kwargs)
        try:
            pk = kwargs['pk']
            instance = get_object_or_404(self.get_model(), pk=pk)
            self.state['instance'] = instance
        except KeyError: pass


class SiteContentFormPreview(UpdateableModelFormPreview):
    form_template = 'content/content_form.html'
    preview_template = 'content/content_preview.html'
    form_base = 'content/content_form_base.html'
    success_view = 'content_detail'

    def done(self, request, cleaned_data):
        model = self.get_model()
        content = model(**cleaned_data)
        if self.is_updating():
            original = self.get_instance()
            content.last_changed_by = request.user
            content.pk = original.pk
            content.created_by = original.created_by
            content.created_date = original.created_date
        else:
            content.created_by = request.user
        content.save()
        return HttpResponseRedirect(reverse(self.success_view, args=(content.id,)))

    def process_preview(self, request, form, context):
        content = form.save(commit=False)
        original = self.get_instance()
        if self.is_updating():
            content.last_changed_by = request.user
            content.last_changed_date = datetime.datetime.now()
            content.created_by = original.created_by
            content.created_date = original.created_date
        else:
            content.created_by = request.user
            content.created_date = datetime.datetime.now()
        context['content'] = content

    def get_context(self, request, form):
        context = super(SiteContentFormPreview, self).get_context(request, form)
        context['form_base'] = self.form_base
        return context
