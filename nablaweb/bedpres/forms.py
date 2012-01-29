# -*- coding: utf-8 -*-


from nablaweb.bedpres.models import BedPres
from nablaweb.events.forms import EventForm
import bpc_core


class BedPresForm(EventForm):
    class Meta(EventForm.Meta):
        model = BedPres

    def __init__(self, *args, **kwargs):
        super(BedPresForm, self).__init__(*args, **kwargs)
        self.fields['event_start'].widget.attrs['readonly'] = True
        self.fields['registration_start'].widget.attrs['readonly'] = True
        self.fields['registration_deadline'].widget.attrs['readonly'] = True
        # self.fields['deregistration_deadline'].widget.attrs['readonly'] = True
        self.fields['location'].widget.attrs['readonly'] = True
        self.fields['has_queue'].widget.attrs['readonly'] = True
        self.fields['places'].widget.attrs['readonly'] = True
        self.fields['registration_required'].widget.attrs['readonly'] = True
        self.fields['bpcid'].widget.attrs['readonly'] = True
