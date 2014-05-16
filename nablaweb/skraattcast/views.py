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

def play(request, skraattcast_id):
    casts = {
        '3': {'htmlid': 'yl17123028', 'url': 'http://yourlisten.com/Skraattcast/skrttcast-sending-2-020514', 'scripturl': 'http://yourlisten.com/embed.js?17123028', 'title': 'Sending 2'},
        '2': {'htmlid': 'yl17106586', 'url': 'http://yourlisten.com/Skraattcast/skrttcast-sending-1-110414', 'scripturl': 'http://yourlisten.com/embed.js?17106586', 'title': 'Sending 1'},
        '1': {'htmlid': 'yl17106567', 'url': 'http://yourlisten.com/Skraattcast/skrttcast-prvesending-destillert-080414', 'scripturl': 'http://yourlisten.com/embed.js?17106567', 'title': 'Prøvesending destillert'}
        }
    return render(request, 'skraattcast/play.html', {"cast": casts[skraattcast_id]})

