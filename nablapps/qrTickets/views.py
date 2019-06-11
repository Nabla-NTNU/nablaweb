from django.shortcuts import render
from django.http import HttpResponse

from .models import QrTicket, QrEvent
from .forms import EmailForm


# Create your views here.
def test(request):
    context = {'hehe': 3}
    return render(request, 'qrTickets/test.html', context)


def generate_tickets(request):
    if request.method == 'GET':
        email_form = EmailForm()
        context = {'email_form': email_form}
        return render(request, 'qrTickets/generate.html', context)
    else:
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            emails = email_form.get_emails()
            email_list = []
            qr_event = email_form.get_qr_event()
            #read emails from string to list
            email_list.append('test@testing.no')
            for email in email_list:
                QrTicket.objects.create(event=qr_event, email = email)
            return HttpResponse("Billetter generert!")


def register_tickets(request, qr_event_id, qr_ticket_id):
    context = {'heh': 2}
    return render(request, 'qrTickets/register.html', context)


