# -*- coding: utf-8 -*-


from django.forms import DateTimeField, DateTimeInput, BooleanField
from nablaweb.events.models import Event
from nablaweb.content.forms import SiteContentForm, SiteContentFormPreview
import datetime


# Hvilke datoformat som aksepteres fra brukeren.
DATE_FORMATS = ['%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M',
                '%Y-%m-%d',
                '%d/%m/%Y %H:%M:%S',
                '%d/%m/%Y %H:%M',
                '%d/%m/%Y',
                '%d/%m/%y %H:%M:%S',
                '%d/%m/%y %H:%M',
                '%d/%m/%y',]

# Standardformatet som brukes til å vise datoer i inputfeltet.
DATE_FORMAT = DATE_FORMATS[1]


class EventDateTimeField(DateTimeField):
    # Bytt datowidget og aksepterte datoformat.
    input_formats = DATE_FORMATS
    widget = DateTimeInput(format=DATE_FORMAT)


class EventForm(SiteContentForm):
    # Spesifiser datowidget og aksepterte datoformat.
    event_start = EventDateTimeField(required=True)
    event_end = EventDateTimeField(required=False)
    registration_start = EventDateTimeField(required=False)
    registration_deadline = EventDateTimeField(required=False)
    deregistration_deadline = EventDateTimeField(required=False)

    # I stedet for NullBooleanField.
    has_queue = BooleanField(required=False)

    # Lar brukeren spesifisere om arrangementet krever påmelding.
    # Internt er dette ekvivalent med at registration_deadline er satt.
    # Dersom registration_required ikke er True ignoreres de mottatte data 
    # for de andre registreringsrelaterte feltene, som i tillegg slettes.
    registration_required = BooleanField(required=False)

    class Meta(SiteContentForm.Meta):
        model = Event

    def clean(self):
        cleaned_data = self.cleaned_data
        # Bind variabler lokalt for å slippe oppslag senere.
        event_start = cleaned_data.get("event_start")
        event_end = cleaned_data.get("event_end")
        registration_required = cleaned_data.get("registration_required")
        places = cleaned_data.get("places")
        registration_deadline = cleaned_data.get("registration_deadline")
        registration_start = cleaned_data.get("registration_start")
        deregistration_deadline = cleaned_data.get("deregistration_deadline")
        has_queue = cleaned_data.get("has_queue")

        # Sjekk om både event_start og event_end har gyldige verdier, og verifiser
        # i så fall at sluttidspunktet ikke er tidligere enn starttidspunktet.
        if event_start and event_end and event_start > event_end:
            self._errors["event_end"] = self.error_class([u'Arrangementslutt må ikke være tidligere enn arrangementstart.'])

        # Tester som kun er relevante dersom påmelding er påkrevd.
        if registration_required is True:
            # Dersom places ikke har noen verdi og ikke har generert andre feil.
            if places is None and "places" not in self._errors:
                self._errors["places"] = self.error_class([u'Antall plasser er påkrevd når "påmelding" er valgt.'])

            # Verifiser at en gyldig registreringsfrist er spesifisert.
            if not registration_deadline and "registration_deadline" not in self._errors:
                self._errors["registration_deadline"] = self.error_class([u'Påmeldingsfrist er påkrevd når "påmelding" er valgt.'])

            # Ved gyldig registreringsfrist, sjekk at denne ikke er etter at arrangementet starter.
            elif event_start and registration_deadline and registration_deadline > event_start:
                self._errors["registration_deadline"] = self.error_class([u'Påmeldingsfrist må ikke være senere enn arrangementstart.'])

            # Sjekk at en eventuell registreringsstart ikke er senere enn registeringsfrist.
            if event_start and registration_start and registration_start > event_start:
                self._errors["registration_start"] = self.error_class([u"Påmeldingsstart må ikke være senere enn påmeldingsfrist."])

            # Sjekk at en eventuell avmeldingsfrist ikke er senere enn arrangementstart.
            if event_start and deregistration_deadline and deregistration_deadline > event_start:
                self._errors["deregistration_deadline"] = self.error_class([u"Avmeldingsfrist må ikke være senere enn arrangementstart."])

            # Sjekk at en eventuell avmeldingsfrist ikke er senere enn en eventuell registreringsstart.
            elif registration_start and deregistration_deadline and registration_start > deregistration_deadline:
                self._errors["deregistration_deadline"] = self.error_class([u"Avmeldingsfrist må ikke være tidligere enn påmeldingsstart."])

            # Sett has_queue til False dersom den av en eller annen grunn ikke skulle mottas.
            if has_queue is None and "has_queue" not in self._errors:
                cleaned_data["has_queue"] = False

        # Dersom påmelding ikke er påkrevd ignoreres innholdet i de andre
        # registreringsrelaterte feltene.
        else:
            # Felt som skal ignoreres.
            field_names = (
                "places",
                "registration_deadline",
                "registration_start",
                "deregistration_deadline",
                "has_queue",
                )
            for name in field_names:
                # Ignorer verdier fra brukeren.
                cleaned_data[name] = None
                # Ignorer feil relatert til feltet.
                if name in self._errors:
                    del self._errors[name]

        del cleaned_data['registration_required']

        return cleaned_data


class EventFormPreview(SiteContentFormPreview):
    form_template = 'events/event_form.html'
    preview_template = 'events/event_preview.html'
    form_base = 'events/event_form_base.html'
    success_view = 'event_detail'

    def get_initial(self, request):
        initial = super(EventFormPreview, self).get_initial(request)
        if self.is_updating():
            original = self.get_instance()
            initial['registration_required'] = original.registration_required()
        return initial
