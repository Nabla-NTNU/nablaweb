from rest_framework import serializers
from nablapps.qrTickets.models import QrTicket


class QrTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrTicket
        fields = ['email', 'registered']
        lookup_field = 'ticket_id'
