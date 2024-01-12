from django.contrib import admin

# Register your models here.
from .models import Mailfeed, Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    list_display = ("mailfeed", "email", "uuid", "created")
    list_select_related = [
        "mailfeed",
    ]
    ordering = ["-mailfeed"]
    list_filter = ["mailfeed", "email"]


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Mailfeed)
