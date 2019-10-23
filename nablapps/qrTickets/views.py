from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import View

from .models import QrTicket, QrEvent
from .forms import EmailForm

# For possible future implementation of ticket inside the mail
from .utils import send_template_email

import random, string


def test(request):
    string_list = ['aaa', 'bbb', 'ccc']
    context = {'hehe': 3, 'string_list': string_list}
    return render(request, 'qrTickets/test.html', context)


def render_ticket(request, qr_event_id, qr_ticket_id):
    ticket_url = 'nabla.no/qrTickets/register/' + str(qr_event_id) + '/' + str(qr_ticket_id)
    url_list = [ticket_url]
    context = {'ticket_url': ticket_url, 'url_list': url_list}
    return render(request, 'qrTickets/render.html', context)


class GenerateTicketsView(PermissionRequiredMixin, View):
    permission_required = "qrTickets.generate_tickets"
    def get(self, request):
        email_form = EmailForm()
        context = {'email_form': email_form}
        return render(request, 'qrTickets/generate.html', context)


    def post(self, request):
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            emails = email_form.get_emails()
            email_list = emails.splitlines()
            qr_event = email_form.get_qr_event()
            for email in email_list:
                # Generates a random string of uppercase letters and numbers, stolen from stack overflow :))
                randstr = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
                ticket = QrTicket.objects.create(event=qr_event, email = email)
                ticket.ticket_id = str(ticket.id) + randstr
                ticket.save()

                subject = 'din nablabillett' #noe mer spes etterhvert
                message = 'Din billett til ' + str(ticket.event) + ' finner du her:\n'
                link = 'nabla.no/qrTickets/render/' + str(qr_event.id) + '/' + ticket.ticket_id
                message += link
                
                try:
                    send_mail(subject, message, "noreply@nablatickets.no", [email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found')
            return HttpResponse("Billetter generert og send på epost!")


class RegisterTicketsView(PermissionRequiredMixin, View):
    permission_required = "qrTickets.register_tickets"
    def get(self, request, qr_event_id, qr_ticket_id):
        context = {'event_id': qr_event_id, 'ticket_id': qr_ticket_id,}
        return render(request, 'qrTickets/register.html', context)
 
    def post(self, request, qr_event_id, qr_ticket_id):
        qr_event = QrEvent.objects.get(pk=qr_event_id)
        try:
            qr_ticket = qr_event.ticket_set.get(ticket_id=qr_ticket_id)
            if qr_ticket.registered:
                return HttpResponse('Allerede registrert. Billetten er oppbrukt.')
            qr_ticket.register()
            qr_ticket.save()
        except QrTicket.DoesNotExist:
            return HttpResponse('Ikke en gyldig billett!')
        return HttpResponse('Billett registrert!')

