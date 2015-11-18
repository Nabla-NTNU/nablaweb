from django.conf import settings
from django.views.generic import View
from django.views import JsonResponse
import os
from subprocess import Popen


def talk_to_bot(request, bot_name):
    user = request.user
    if user.is_authenticated():
        raw_input = request.GET.get('input')
        send_to_bot(bot_name, raw_input)


LEGAL_CHARS = 'abcdefghijklmnopqrstuvwxyz? '


def sanitize(input):
    clean_text = ''
    for c in input:
        if c in LEGAL_CHARS:
            clean_text += c
    return clean_text


def send_to_bot(bot_name, raw_input):
    bot = BOTS.get(bot_name)
    return bot(raw_input)


def annabell(input):
    input = sanitize(input)
    dir = settings.ANNABELL_ROOT
    process = Popen(dir+"annabell")
    out, err = Popen.communicate((input=input)
    return out


BOTS = {"annabell": annabell}

