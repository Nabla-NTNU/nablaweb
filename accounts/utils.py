# -*- coding: utf-8 -*-

from django.template import loader
from django.contrib.auth.models import UserManager
import re


def activate_user_and_create_password(user):
    studmail = user.username+"@stud.ntnu.no"
    if not(user.email):
        user.email = studmail

    user_manager = UserManager()
    password = user_manager.make_random_password()
    user.set_password(password)
    user.is_active = True
    user.save()
    return password


def send_activation_email(user, password):
    t = loader.get_template('accounts/registration_email.txt')
    email_text = t.render({"username": user.username,
                           "password": password})
    user.email_user('Bruker på nabla.no', email_text)


def extract_usernames(string):
    from accounts.models import NablaUser

    m = re.findall('([a-z]+)@', string, re.IGNORECASE)
    for u in m:
        NablaUser.objects.get_or_create(username=u)
