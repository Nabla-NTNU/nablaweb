from django.contrib import admin


class ContentAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.last_changed_by = request.user

        # Hvis objekter ikke er laget av noen, legg til denne brukeren
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()
