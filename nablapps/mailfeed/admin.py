from django.contrib import admin

# Register your models here.
from .models import Mailfeed, Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def short_description(self, com):
        return (com.story[:23] + "...") if len(com.story) > 25 else com.story

    def full_user_name(self, com):
        return com.user.get_full_name()

    list_display = ("mailfeed", "email", "uuid", "created")
    list_select_related = [
        "mailfeed",
    ]
    ordering = ["-mailfeed"]
    list_filter = ["mailfeed", "email"]


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Mailfeed)
