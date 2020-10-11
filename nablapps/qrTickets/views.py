import random
import string

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .forms import EmailForm, EventForm
from .models import QrEvent, QrTicket

from rest_framework import generics
from nablapps.qrTickets.serializers import QrTicketSerializer
from rest_framework import permissions


def render_ticket(request, qr_event_id, qr_ticket_id):
    ticket_url = (
        "nabla.no/qrTickets/register/" + str(qr_event_id) + "/" + str(qr_ticket_id)
    )
    url_list = [ticket_url]
    context = {"ticket_url": ticket_url, "url_list": url_list}
    return render(request, "qrTickets/render.html", context)


class QrEventListView(ListView):
    model = QrEvent
    template_name = "qrTickets/event_list.html"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class CreateEventView(PermissionRequiredMixin, View):
    permission_required = "qrTickets.generate_tickets"

    def get(self, request):
        event_form = EventForm()
        context = {"event_form": event_form}
        return render(request, "qrTickets/create_event.html", context)
        
    def post(self, request):
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            nabla_event = event_form.get_nabla_event()
            event_name = event_form.get_event_name()

            # Create qr event
            event = QrEvent.objects.create(name=event_name, nabla_event=nabla_event)
            event.save()
        return HttpResponse("QrEvent successfully created!")


class EventDetailView(PermissionRequiredMixin, View):
    permission_required = "qrTickets.generate_tickets"

    def get(self, request, pk):
        email_form = EmailForm()
        context = {"email_form": email_form}
        context['event'] = QrEvent.objects.get(pk=pk)
        return render(request, "qrTickets/generate.html", context)

    def post(self, request, pk):
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            emails = email_form.get_emails()
            email_list = emails.splitlines()
            qr_event = QrEvent.objects.get(pk=pk)
            for email in email_list:
                # Generates a random string of uppercase letters and numbers, stolen from stack overflow :))
                randstr = "".join(
                    random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                    for _ in range(10)
                )
                ticket = QrTicket.objects.create(event=qr_event, email=email)
                ticket.ticket_id = str(ticket.id) + randstr
                ticket.save()

                subject = "din nablabillett"  # noe mer spes etterhvert
                message = "Din billett til " + str(ticket.event) + " finner du her:\n"
                link = (
                    "nabla.no/qrTickets/render/"
                    + str(qr_event.id)
                    + "/"
                    + ticket.ticket_id
                )
                message += link

                try:
                    send_mail(
                        subject,
                        message,
                        "noreply@nablatickets.no",
                        [email],
                        fail_silently=False,
                    )
                except BadHeaderError:
                    return HttpResponse("Invalid header found")
            return HttpResponse("Billetter generert og send på epost!")


class RegisterTicketsView(PermissionRequiredMixin, View):
    permission_required = "qrTickets.register_tickets"

    def get(self, request, qr_event_id, qr_ticket_id):
        context = {
            "event_id": qr_event_id,
            "ticket_id": qr_ticket_id,
        }
        return render(request, "qrTickets/register.html", context)

    def post(self, request, qr_event_id, qr_ticket_id):
        qr_event = QrEvent.objects.get(pk=qr_event_id)
        try:
            qr_ticket = qr_event.ticket_set.get(ticket_id=qr_ticket_id)
            if qr_ticket.registered:
                return HttpResponse("Allerede registrert. Billetten er oppbrukt.")
            qr_ticket.register()
            qr_ticket.save()
        except QrTicket.DoesNotExist:
            return HttpResponse("Ikke en gyldig billett!")
        return HttpResponse("Billett registrert!")


class TicketList(generics.ListCreateAPIView):
    queryset = QrTicket.objects.all()
    serializer_class = QrTicketSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete ticket.
    """
    queryset = QrTicket.objects.all()
    serializer_class = QrTicketSerializer
    lookup_field = 'ticket_id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UpdateTicketsView(generics.UpdateAPIView):
    """
    API endpoint that allows tickets to be updated.
    """
    queryset = QrTicket.objects.all()
    serializer_class = QrTicketSerializer
    lookup_field = 'ticket_id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


