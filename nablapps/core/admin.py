"""
Utilities for admin
"""

from django.contrib import admin
from django.contrib.admin.models import LogEntry


class ChangedByMixin:  # pylint: disable=too-few-public-methods
    """
    To be mixed into a subclass of admin.ModelAdmin

    It makes sure that when a staff user creates or changes
    an instance of a model in the admin interface the instance is
    also updated with info about who created or changed it.

    Assumes that the model has fields corresponding to
    the TimeStamped abstract model.
    """

    def save_model(self, request, obj, form, change):
        """
        Overrides save_model from admin.ModelAdmin
        """
        obj.last_changed_by = request.user

        # Set created_by if not already set.
        # This will most likely only happen when the object is created,
        # but if the object was not created in the admin interface then
        # the next person to change it in admin will be set as the creator.
        if getattr(obj, "created_by", None) is None:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class LogEntryAdmin(admin.ModelAdmin):
    model = LogEntry
    readonly_fields = list_display = (
        "user",
        "content_type",
        "object_id",
        "object_repr",
        "action_flag",
        "change_message",
        "action_time",
    )
    list_select_related = ("user", "content_type")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    list_filter = ("content_type",)
    date_hierarchy = "action_time"


admin.site.register(LogEntry, LogEntryAdmin)
