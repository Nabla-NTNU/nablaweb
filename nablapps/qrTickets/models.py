from django.db import models

from nablapps.events.models.event import Event


class QrEvent(models.Model):
    name = models.CharField(max_length=100)
    nabla_event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="qr_event_set",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name


class QrTicket(models.Model):
    event = models.ForeignKey(
        QrEvent, on_delete=models.CASCADE, related_name="ticket_set"
    )
    email = models.EmailField(blank=False)
    registered = models.BooleanField(default=False)
    ticket_id = models.CharField(max_length=200)

    def __str__(self):
        return self.email

    def get_email(self):
        return self.email

    def register(self):
        self.registered = True

    def get_ticket_id(self):
        return self.ticket_id

    class Meta:
        permissions = [
            ("generate_tickets", "can generate qr tickets"),
            ("register_tickets", "can register qr tickets"),
        ]
