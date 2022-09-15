from collections import defaultdict
from functools import partial
from io import StringIO

from django.contrib import admin
from django.db import transaction
from django.http import HttpResponse

from .models import ComMembership, ComPage


class ComPageAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Komiteside"
        verbose_name_plural = "Komitesider"
        fields = "__all__"


class ComMembershipAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Komitemedlem"
        verbose_name_plural = "Komitemedlemmer"

    def export_all_active_members(modeladmin, request, queryset):
        """Download a file mapping each committee to a list of active members"""
        # Map committee_name -> list of active members
        committee_member_mapping = defaultdict(list)

        all_members = ComMembership.objects.all()

        # We ignore the queryset, and export all active members
        active_members = all_members.select_related("user", "com").filter(
            is_active=True, user__email__isnull=False
        )

        for membership in active_members:
            committee_member_mapping[membership.com.name].append(membership.user.email)

        output_stream = StringIO()
        write_to_attachment = partial(print, file=output_stream)

        # Write some stats
        write_to_attachment(
            f"Total members (active and inactive): {all_members.count()}"
        )
        write_to_attachment(f"Active members with emails: {active_members.count()}")
        write_to_attachment(
            f"#Committees with active members: {len(committee_member_mapping)}"
        )
        write_to_attachment(
            f"Committees with active members: {', '.join(committee_member_mapping.keys())}"
        )
        write_to_attachment("\n\n")

        for committee, emails in committee_member_mapping.items():
            write_to_attachment(f"**{committee}**:")
            for email in emails:
                write_to_attachment(email)
            write_to_attachment("------------------------\n")

        output_stream.seek(0)
        response = HttpResponse(output_stream, content_type="text")
        response[
            "Content-Disposition"
        ] = "attachment; filename=active_committee_members.txt"
        return response

    @transaction.atomic
    def set_active(modeladmin, request, queryset):
        """Set all selected members as active, and add to group"""
        queryset.update(is_active=True)
        for membership in queryset:
            membership.com.user_set.add(membership.user)

    @transaction.atomic
    def set_inactive(modeladmin, request, queryset):
        """Set all selected members as inactive, and remove from group"""
        queryset.update(is_active=False)
        for membership in queryset:
            membership.com.user_set.remove(membership.user)

    def short_description(self, com):
        return (com.story[:23] + "...") if len(com.story) > 25 else com.story

    def full_user_name(self, com):
        return com.user.get_full_name()

    export_all_active_members.short_name = "Eksportér alle aktive medlemmer"
    set_active.short_name = "Markér som aktiv"
    set_inactive.short_name = "Markér som inaktiv"

    list_display = ("full_user_name", "user", "com", "joined_date", "short_description")
    list_select_related = ("user", "com")
    ordering = ["-com"]
    list_filter = ["is_active", "com"]
    actions = [set_active, set_inactive, export_all_active_members]


class CommitteeAdmin(admin.ModelAdmin):
    class Meta:
        fields = "__all__"


admin.site.register(ComPage, ComPageAdmin)
admin.site.register(ComMembership, ComMembershipAdmin)
