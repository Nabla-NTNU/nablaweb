
from contextlib import suppress
from django.contrib import messages
from django.contrib.messages.api import MessageFailure
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils.safestring import mark_safe
from django.utils.html import escape


def login_message(sender, request, user, **kwargs):
    with suppress(MessageFailure):
        msg = 'Velkommen inn <strong>' + escape(user.username) + '</strong>'
        messages.info(request, mark_safe(msg))


def logout_message(sender, request, user, **kwargs):
    with suppress(MessageFailure):
        msg  = '<strong>' + escape(user.username) + '</strong> ble logget ut'
        messages.info(request, mark_safe(msg))


def register_signals():
    user_logged_in.connect(login_message)
    user_logged_out.connect(logout_message)
