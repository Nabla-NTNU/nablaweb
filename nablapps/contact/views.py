import datetime
import random

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import resolve

from click import style

from .forms import ContactForm, FeedbackForm, ForCompanyForm, RoomForm


def contact(request):
    spam_check = False
    if request.method != "POST":
        test_val = random.randint(0, 20)
        context = make_contact_context(request, spam_check, test_val)
        return render(request, "contact/contact.html", context)
    else:
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            # spam check
            if contact_form.get_right_answer() == contact_form.get_answer():
                # Sends mail
                subject, message, email = contact_form.process()
                if not email:
                    email = "noreply@anonym.nabla.no"
                try:
                    if contact_form.get_reciever() == "PostKom":
                        # endret fra forslagskasse.postkom@nabla.no
                        mailadress = "postkom@nabla.no"
                    elif contact_form.get_reciever() == "ITV ved IFY":
                        mailadress = "fysikk@sr-nv.no"
                    elif contact_form.get_reciever() == "ITV ved IMF":
                        mailadress = "imf@sr-ie.no"
                    else:
                        # endret fra forslagskasse.styret@nabla.no - føler det er mer hensiktsmessig at vi får dem på hovedmailen til styret (Nestleder 2022)
                        # Jeg tenker det samme om PostKom
                        mailadress = "nabla@nabla.no"

                    send_mail(
                        subject, message, email, [mailadress], fail_silently=False
                    )
                except BadHeaderError:
                    return HttpResponse("Invalid header found")
                return HttpResponseRedirect("/contact/success/")
            else:
                spam_check = True
                test_val = random.randint(0, 20)
                context = make_contact_context(request, spam_check, test_val)
                return render(request, "contact/contact.html", context)


def feedback(request, template="feedback.html", send_to="webkom@nabla.no"):
    spam_check = False
    if request.method != "POST":
        test_val = random.randint(0, 20)
        context = make_feedback_context(request, spam_check, test_val)
        return render(request, "contact/" + template, context)
    else:
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            # spam check
            if feedback_form.get_right_answer() == feedback_form.get_answer():
                # Sends mail
                subject, message, email = feedback_form.process()
                if resolve(request.path_info).url_name == "gullkorn":
                    # remove "your_name" from message
                    message = "\n".join(message.split("\n")[:-1])
                    message = f"<<{message}>> -{subject}"
                    subject = "Sitat " + datetime.date.today().strftime("%d.%m.%y")

                try:
                    send_mail(subject, message, email, [send_to], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse("Ivalid header found")
                if resolve(request.path_info).url_name == "gullkorn":
                    return HttpResponseRedirect("/contact/success_gullkorn/")
                    # sjekker om man leverer et skjema
                return HttpResponseRedirect("/contact/success/")
            else:
                spam_check = True
                test_val = random.randint(0, 20)
                context = make_feedback_context(request, spam_check, test_val)
                return render(request, "contact/" + template, context)


def roombooking(request, template="rombooking.html", send_to="nestleder@nabla.no"):
    spam_check = False
    if request.method != "POST":
        test_val = random.randint(0, 20)
        context = make_roombooking_context(request, spam_check, test_val)
        return render(request, "contact/" + template, context)
    else:
        room_form = RoomForm(request.POST)
        if room_form.is_valid():
            # spam check
            if room_form.get_right_answer() == room_form.get_answer():
                # Sends mail
                subject, message, email = room_form.process()
                if resolve(request.path_info).url_name == "gullkorn":
                    # remove "your_name" from message
                    message = "\n".join(message.split("\n")[:-1])
                    message = f"<<{message}>> -{subject}"
                    subject = "Sitat " + datetime.date.today().strftime("%d.%m.%y")

                try:
                    send_mail(subject, message, email, [send_to], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse("Ivalid header found")
                if resolve(request.path_info).url_name == "gullkorn":
                    return HttpResponseRedirect("/contact/success_gullkorn/")
                    # sjekker om man leverer et skjema
                return HttpResponseRedirect("/contact/success/")
            else:
                spam_check = True
                test_val = random.randint(0, 20)
                context = make_feedback_context(request, spam_check, test_val)
                return render(request, "contact/" + template, context)


def success(request):
    return render(request, "contact/success.html")


def success_gullkorn(request):
    return render(request, "contact/success_gullkorn.html")


#######################################################################


# The two functions below are not views, they return appropriate context for feedback and contact view
def make_contact_context(request, spam_check, test_val):
    board_emails = (
        ("Hele styret", "nabla"),
        ("Leder", "leder"),
        ("Nestleder", "nestleder"),
        ("Faddersjef/sekretær", "sekretaer"),
        ("Kasserer", "kasserer"),
        ("Kommunikasjonssjef", "komsjef"),
        ("Bedkomsjef", "bedriftskontakt"),
        ("Arrangementsjef", "arrsjef"),
        ("Jubileumssjef", "jubileumssjef"),
    )
    nabla_pos_emails = (
        ("Alle gruppeledere", "gruppeledere"),
        ("Ambassadør", "ambassador"),
        ("Leder av ProKom", "leder.prokom"),
        ("Leder av QuizKom", "quizkom"),
        ("Kjellersjef", "kjellersjef"),
        ("Leder av Koreolis", "koreolis.kraften"),
        ("Redaktør", "redaktor"),
        ("Leder av Reka", "reka"),
        ("Leder av Reven", "reven"),
        ("Leder av Skråttcast", "skraattcast"),
        ("Leder av Gravitones", "leder.gravitones"),
        ("Leder av the Stokes", "lederstokes"),
        ("Musikalsk leder - Maxwells Muntre Musikanter", "maxwells.muntre"),
        ("Økonomiansvarlig i bedriftskontakten", "bnokonomi"),
        ("Revysjef", "revy"),
        ("Bryggemester", "bryggemester"),
        ("Leder av KontorKom", "leder.kontorkom"),
        ("Websjef", "websjef"),
    )
    group_emails = (
        ("PostKom", "postkom"),
        ("Arrkom", "arrkom"),
        ("BN - Bedriftkontakten Nabla", "bedkom"),
        ("Eurekakom", "eureka"),
        ("Educom", "educom"),
        ("ProKom", "prokom"),
        ("Redaksjonen", "nabladet"),
        ("WebKom", "webkom"),
        ("Excom17", "ekskom2019"),
        ("Excom18", "excom18"),
        ("Kontorkom", "kontorkom"),
        ("Koreolis", "koreolis"),
        ("nablarevyen", "revy-alle"),
        ("the Gravitones", "gravitones"),
        ("the Stokes", "thestokes"),
        ("utfluks", "utfluks"),
        ("Kjellersamarbeidet (Nabla, HC, Janus)", "kjellern.hk18"),
    )

    if request.user.is_authenticated:
        # skjema uten navn og e-post
        contact_form = ContactForm(
            initial={
                "your_name": request.user.get_full_name(),
                "email": request.user.email,
                "right_answer": test_val,
                "spam_check": "ditt svar",
            }
        )

    else:
        # tomt skjema
        contact_form = ContactForm(initial={"right_answer": test_val})

    context = {
        "contact_form": contact_form,
        "spam_check": spam_check,
        "test_val": test_val,
    }
    contact_form.fields[
        "spam_check"
    ].label = (
        f"Hva er kvadratroten av {test_val} ganget med kvadratroten av {test_val}? "
    )
    contact_form.fields[
        "spam_check"
    ].help_text = "Skriv inn svaret over for å verifisere at du er et menneske"
    context["board_emails"] = board_emails
    context["nabla_pos_emails"] = nabla_pos_emails
    context["group_emails"] = group_emails
    return context


def make_feedback_context(request, spam_check, test_val):
    if request.user.is_authenticated:
        # skjema uten navn og e-post
        feedback_form = FeedbackForm(
            initial={
                "your_name": request.user.get_full_name(),
                "email": request.user.email,
                "right_answer": test_val,
            }
        )

    else:
        # tomt skjema
        feedback_form = FeedbackForm(initial={"right_answer": test_val})
    feedback_form.fields[
        "spam_check"
    ].label = (
        f"Hva er kvadratroten av {test_val} ganget med kvadratroten av {test_val}? "
    )
    feedback_form.fields[
        "spam_check"
    ].help_text = "Skriv inn svaret over for å verifisere at du er et menneske"
    context = {
        "feedback_form": feedback_form,
        "spam_check": spam_check,
        "test_val": test_val,
    }
    return context


def make_roombooking_context(request, spam_check, test_val):
    if request.user.is_authenticated:
        # skjema uten navn og e-post
        room_form = RoomForm(
            initial={
                "your_name": request.user.get_full_name(),
                "email": request.user.email,
                "right_answer": test_val,
            }
        )

    else:
        # tomt skjema
        room_form = RoomForm(initial={"right_answer": test_val})
    room_form.fields[
        "spam_check"
    ].label = (
        f"Hva er kvadratroten av {test_val} ganget med kvadratroten av {test_val}? "
    )
    room_form.fields[
        "spam_check"
    ].help_text = "Skriv inn svaret over for å verifisere at du er et menneske"
    context = {
        "room_form": room_form,
        "spam_check": spam_check,
        "test_val": test_val,
    }
    return context


def for_bedrifter(request, template="for_bedrifter.html", send_to="bedkom@nabla.no"):
    return render(request, "contact/" + template)
