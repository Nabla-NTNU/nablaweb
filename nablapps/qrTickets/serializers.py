from rest_framework import serializers

from nablapps.qrTickets.models import QrTicket


class QrTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrTicket
        fields = ["registered", "email", "ticket_id"]
        read_only_fields = ["email", "ticket_id"]
        lookup_field = "ticket_id"
