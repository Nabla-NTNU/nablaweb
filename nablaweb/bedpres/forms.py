# -*- coding: utf-8 -*-


from nablaweb.bedpres.models import BedPres
from nablaweb.events.forms import EventForm, EventFormPreview
import datetime
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


# TODO: Tenk over muligheten for POST-hacks for å endre felt som er
# 'readonly' i BedPresForm.
class BedPresFormPreview(EventFormPreview):
    form_template = 'bedpres/bedpres_form.html'
    preview_template = 'bedpres/bedpres_preview.html'
    form_base = 'bedpres/bedpres_form_base.html'
    success_detail = 'bedpres_detail'

    def get_initial(self, request):
        initial = super(BedPresFormPreview, self).get_initial(request)
        bpc_info = self.state['bpc_info']
        field_tuple = ('event_start', 'registration_start',
                       'registration_deadline', 'location',
                       'has_queue', 'places', 'bpcid')
        for field in field_tuple:
            initial[field] = bpc_info[field]
        initial['registration_required'] = True
        if not self.is_updating():
            initial['headline'] = bpc_info['headline']
            initial['lead_paragraph'] = ''.join((
                    bpc_info['description'],
                    '\n\n[img]',bpc_info['logo'], '[/img]',
                    '\n\n[url=',bpc_info['web_page'],']',
                    bpc_info['headline'], '[/url]\n',
                    ))
        return initial

    def parse_params(self, *args, **kwargs):
        super(BedPresFormPreview, self).parse_params(*args, **kwargs)
        if self.is_updating():
            bpcid = self.state['instance'].bpcid
        else:
            bpcid = kwargs['bpcid']
        bpc_info = bpc_core.get_single_event(bpcid)
        self.state['bpc_info'] = bpc_info
