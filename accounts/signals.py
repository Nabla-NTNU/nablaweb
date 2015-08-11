
from django.contrib import messages
from django.contrib.messages.api import MessageFailure
from django.contrib.auth.signals import user_logged_in, user_logged_out

def login_message(sender, request, user, **kwargs):
    try:
        messages.add_message(request, messages.INFO, u'Velkommen inn <strong>{}</strong>'.format(user.username))
    except MessageFailure:
        pass

def logout_message(sender, request, user, **kwargs):
    try:
        messages.add_message(request, messages.INFO, u'<strong>{}</strong> ble logget ut'.format(user.username))
    except MessageFailure:
        pass

def register_signals():
    user_logged_in.connect(login_message)
    user_logged_out.connect(logout_message)
