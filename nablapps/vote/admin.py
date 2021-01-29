from django.contrib import admin

from .models import Alternative, Voting, VotingEvent

admin.site.register(Voting)
admin.site.register(Alternative)
admin.site.register(VotingEvent)
