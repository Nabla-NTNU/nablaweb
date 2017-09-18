class ChangedByMixin(object):
    def save_model(self, request, obj, form, change):
        obj.last_changed_by = request.user

        # Update created_by
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        super(ChangedByMixin, self).save_model(request, obj, form, change)
