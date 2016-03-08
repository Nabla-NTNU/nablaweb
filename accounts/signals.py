
from contextlib import suppress
from django.contrib import messages
from django.contrib.messages.api import MessageFailure
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils.safestring import mark_safe


def login_message(sender, request, user, **kwargs):
    with suppress(MessageFailure):
        messages.info(request, mark_safe(u'Velkommen inn <strong>{user.username}</strong>'.format(user=user)))


def logout_message(sender, request, user, **kwargs):
    with suppress(MessageFailure):
        messages.info(request, mark_safe(u'<strong>{user.username}</strong> ble logget ut'.format(user=user)))


def register_signals():
    user_logged_in.connect(login_message)
    user_logged_out.connect(logout_message)
