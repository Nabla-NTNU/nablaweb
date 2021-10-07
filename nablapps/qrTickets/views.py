import random
import string

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from nablapps.qrTickets.serializers import QrTicketSerializer

from .forms import EmailForm, EventForm
from .models import QrEvent, QrTicket


class ScanTicketView(TemplateView):
    template_name = "qrTickets/scan.html"


def render_ticket(request, qr_event_id, qr_ticket_id):
    ticket_url = (
        "nabla.no/qrTickets/register/" + str(qr_event_id) + "/" + str(qr_ticket_id)
    )
    url_list = [ticket_url]
    context = {"ticket_url": ticket_url, "url_list": url_list}
    return render(request, "qrTickets/render.html", context)


class QrEventListView(PermissionRequiredMixin, ListView):
    permission_required = "qrTickets.generate_tickets"
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
        return redirect(reverse("qr-event-list"))


class EventDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "qrTickets.generate_tickets"

    def get(self, request, pk):
        email_form = EmailForm()
        context = {"email_form": email_form}
        qr_event = QrEvent.objects.get(pk=pk)
        context["event"] = qr_event
        context["email_list"] = qr_event.ticket_set.all()
        return render(request, "qrTickets/qr_event_detail.html", context)

    def post(self, request, pk):
        qr_event = QrEvent.objects.get(pk=pk)
        email_list = []
        if qr_event.nabla_event:
            email_list += qr_event.nabla_event.users_attending_emails()
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            emails = email_form.get_emails()
            email_list += emails.splitlines()
        already_recieved_list = [
            ticket.__str__() for ticket in qr_event.ticket_set.all()
        ]
        for email in email_list:
            if email not in already_recieved_list:
                randstr = "".join(
                    random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                    for _ in range(11)
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
        return redirect(reverse("qr-event-detail", kwargs={"pk": pk}))


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


class UpdateTicketsView(generics.UpdateAPIView):
    """
    API endpoint that allows tickets to be updated.
    """

    queryset = QrTicket.objects.all()
    serializer_class = QrTicketSerializer
    lookup_field = "ticket_id"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, ticket_id):
        try:
            ticket = QrTicket.objects.get(ticket_id=ticket_id)
        except QrTicket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = QrTicketSerializer(ticket, data=request.data)
        if ticket.registered:
            return Response(status=status.HTTP_208_ALREADY_REPORTED)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
