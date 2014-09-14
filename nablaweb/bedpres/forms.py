# -*- coding: utf-8 -*-


from django import forms
from bedpres.models import BedPres
from events.forms import EventForm
import bpc_core


class BedPresForm(EventForm):
    class Meta(EventForm.Meta):
        model = BedPres
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BedPresForm, self).__init__(*args, **kwargs)

        # Disse er readonly fordi de er hentet fra BPC

        self.fields['event_start'].widget.attrs['readonly'] = True
        self.fields['registration_start'].widget.attrs['readonly'] = True
        self.fields['registration_deadline'].widget.attrs['readonly'] = True
        self.fields['deregistration_deadline'].widget.attrs['readonly'] = True
        self.fields['location'].widget.attrs['readonly'] = True
        self.fields['has_queue'].widget.attrs['readonly'] = True
        self.fields['places'].widget.attrs['readonly'] = True
        self.fields['registration_required'].widget.attrs['readonly'] = True
        self.fields['bpcid'].widget.attrs['readonly'] = True


class BPCForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # http://jacobian.org/writing/dynamic-form-generation/

        super(BPCForm, self).__init__(*args, **kwargs)

        # Lag en liste med bedpresser som ikke finnes lokalt.
        bpc_events = bpc_core.get_events()['event']
        bpc_ids = [event['id'] for event in bpc_events]
        local_events = BedPres.objects.filter(bpcid__in=bpc_ids)
        local_ids = [event.bpcid for event in local_events]
        print local_ids
        available_events = filter(lambda e: e['id'] not in local_ids, bpc_events)

        choices = [(event['id'], event['title']) for event in available_events]

        self.available_events = available_events
        self.fields['events'] = forms.MultipleChoiceField(required=False, label="Tilgjengelig fra BPC", choices=choices, widget=forms.CheckboxSelectMultiple)
