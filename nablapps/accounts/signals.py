from contextlib import suppress

from django.contrib import messages
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.messages.api import MessageFailure
from django.utils.html import escape
from django.utils.safestring import mark_safe


def login_message(sender, request, user, **kwargs):
    with suppress(MessageFailure):
        msg = f"Velkommen inn <strong>{escape(user.username)}</strong>"
        messages.info(request, mark_safe(msg))

    # with suppress(MessageFailure):
    #     msg = f"Vil du få sjansen til å vinne gavekort på 250 kr, og mange andre kule premier? Sjekk ut innkallingen til eSKE da vel! " kan også brukes til annet
    #     messages.error(request, mark_safe(msg))


def logout_message(sender, request, user, **kwargs):
    with suppress(MessageFailure):
        msg = f"<strong>{escape(user.username)} </strong> ble logget ut"
        messages.info(request, mark_safe(msg))

    # with suppress(MessageFailure):
    #     msg = f"Vil du få sjansen til å vinne gavekort på 250 kr, og mange andre kule premier? Sjekk ut innkallingen til eSKE da vel! " kan også brukes til annet
    #     messages.error(request, mark_safe(msg))


def register_signals():
    user_logged_in.connect(login_message)
    user_logged_out.connect(logout_message)
