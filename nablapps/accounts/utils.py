import re

from django.contrib.auth.models import UserManager
from django.template import loader


def activate_user_and_create_password(user):
    studmail = user.username + "@stud.ntnu.no"
    if not (user.email):
        user.email = studmail

    user_manager = UserManager()
    password = user_manager.make_random_password()
    user.set_password(password)
    user.is_active = True
    user.save()
    return password


def send_activation_email(user, password):
    t = loader.get_template("accounts/registration_email.txt")
    email_text = t.render({"username": user.username, "password": password})
    user.email_user("Bruker på nabla.no", email_text)


def extract_usernames(string, fysmat_class=None):
    from .models import NablaUser, RegistrationRequest

    m = re.findall("([a-z]+)@", string, re.IGNORECASE)
    for u in m:
        requests = RegistrationRequest.objects.filter(username=u)

        if requests:
            requests.last().approve_request()
            for r in requests:
                r.delete()

        new_user, was_created = NablaUser.objects.get_or_create(username=u)
        if not was_created:
            continue

        if fysmat_class is not None:
            fysmat_class.user_set.add(new_user)

        new_user.is_active = False
        new_user.save()
