# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    casts = [
            {'id': 3, 'title': u'Sending 2', 'date': '02.05.14', 'description': u'Alexander, Kristian og Petter tar for seg mindre aktuelle nyhetssaker og innsendte… spørsmål. Byr også på en tøff konkurranse med mye på spill.'},
            {'id': 2, 'title': u'Sending 1', 'date': '11.04.14', 'description': u'Alexander, Grigory og Petter utgjør denne første ordinære sendingen av Skråttcast.… Finurlige dilemmaer er i fokus.'},
            {'id': 1, 'title': u'Prøvesending destillert', 'date': '08.04.14', 'description': u'Per Ivar, Kristian og Petter prøver ut såkalt "podcast". Innsendte spørsmål og høyverdig… improvisasjon rent innholdsmessig er bare noen av de spennende og hårreisende stikkordene på agendaen.'}
    ]
    return render(request, 'skraattcast/index.html', {"casts": casts})

