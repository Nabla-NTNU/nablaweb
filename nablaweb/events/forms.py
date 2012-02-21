# -*- coding: utf-8 -*-


from django.forms import SplitDateTimeField, BooleanField 
from django.contrib.admin.widgets import AdminSplitDateTime
from nablaweb.events.models import Event
from nablaweb.news.forms import NewsForm, CustomSplitDateTimeWidget
from nablaweb.news.forms import NewsCharField as EventCharField
import datetime


# Hvilke datoformat som aksepteres fra brukeren.
DATE_FORMATS = ['%Y-%m-%d',
                '%d/%m/%Y',
                '%d/%m/%y',
                '%d.%m.%Y',
                '%d.%m.%y',
                '%d.%n.%Y',
                '%d.%n.%y',]

TIME_FORMATS = ['%H:%M:%S',
                '%H:%M',
                '%H',]


class EventSplitDateTimeField(SplitDateTimeField):
    default_error_messages = {
        'invalid_date': u'Ugyldig dato. Prøv formatet "DD.MM.ÅÅÅÅ".',
        'invalid_time': u'Ugyldig tid. Prøv formatet "HH:MM".',
        'required': u'Dette tidspunktet er påkrevd.',
        }

    def __init__(self, *args, **kwargs):
        kwargs.update(input_date_formats=DATE_FORMATS,
                      input_time_formats=TIME_FORMATS,
                      widget=AdminSplitDateTime())
        super(EventSplitDateTimeField, self).__init__(*args, **kwargs)


class EventForm(NewsForm):
    # Spesifiser datowidget og aksepterte datoformat.
    event_start = EventSplitDateTimeField(required=True, label="Starter")
    event_end = EventSplitDateTimeField(required=False, label="Slutter")
    registration_start = EventSplitDateTimeField(required=False, label="Påmelding åpner")
    registration_deadline = EventSplitDateTimeField(required=False, label="Påmelding stenger")
    deregistration_deadline = EventSplitDateTimeField(required=False, label="Avmelding stenger")

    # For å få norske feilmeldinger.
    location = EventCharField(label="Sted")

    # I stedet for NullBooleanField.
    has_queue = BooleanField(required=False, label="Har venteliste", help_text="Hvis arrangementet har venteliste, går det ann å melde seg på selv etter at det er fullt. Man havner da på venteliste, og blir automatisk meldt på om det blir ledig.")

    # Lar brukeren spesifisere om arrangementet krever påmelding.
    # Internt er dette ekvivalent med at registration_deadline er satt.
    # Dersom registration_required ikke er True ignoreres de mottatte data 
    # for de andre registreringsrelaterte feltene, som i tillegg slettes.
    registration_required = BooleanField(required=False, label="Registrering kreves")

    class Meta(NewsForm.Meta):
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
