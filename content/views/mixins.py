from django.core.urlresolvers import reverse


class AdminLinksMixin(object):
    """
    Adds links to the admin page for an object to the context.

    Meant to be used together with DetailView.
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        view_name = "admin:{app_label}_{model_name}_{action}"
        context["change_url"] = reverse(view_name.format(action="change", **locals()), args=[self.object.id])
        context["delete_url"] = reverse(view_name.format(action="delete", **locals()), args=[self.object.id])
        return context


class ViewAddMixin(object):
    """
    Adds one view to the object each time the object is dispatched
    """

    def get_context_data(self, *args, **kwargs):
        self.object.add_view()
        return super().get_context_data(*args, **kwargs)
