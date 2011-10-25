# -*- coding: utf-8 -*-


from nablaweb.bedpres.models import BedPres
from nablaweb.events.forms import EventForm, EventFormPreview
import datetime


class BedPresForm(EventForm):
    class Meta(EventForm.Meta):
        model = BedPres

    def clean(self):
        print "Hello, World!"
        return super(BedPresForm, self).clean()


class BedPresFormPreview(EventFormPreview):
    form_template = 'bedpres/bedpres_form.html'
    preview_template = 'bedpres/bedpres_preview.html'
    form_base = 'bedpres/bedpres_form_base.html'
    success_detail = 'bedpres_detail'
