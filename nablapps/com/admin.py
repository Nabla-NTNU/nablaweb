from django.contrib import admin

from .models import ComMembership, ComPage


class ComPageAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Komiteside"
        verbose_name_plural = "Komitesider"
        fields = "__all__"


class ComMembershipAdmin(admin.ModelAdmin):
    list_display = ("full_user_name", "user", "com", "joined_date", "short_description")
    ordering = ["-com"]
    list_filter = ["com"]

    def short_description(self, com):
        return (com.story[:23] + "...") if len(com.story) > 25 else com.story

    def full_user_name(self, com):
        return com.user.get_full_name()

    class Meta:
        verbose_name = "Komitemedlem"
        verbose_name_plural = "Komitemedlemmer"


class CommitteeAdmin(admin.ModelAdmin):
    class Meta:
        fields = "__all__"


admin.site.register(ComPage, ComPageAdmin)
admin.site.register(ComMembership, ComMembershipAdmin)
