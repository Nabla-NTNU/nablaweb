# pylint: disable=C0111
"""
Mixin classes for views
"""
from django.urls import reverse
from django.http import HttpResponseForbidden


class AdminLinksMixin:
    """
    Adds links to the admin page for an object to the context.

    Meant to be used together with DetailView.
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pylint: disable=protected-access
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        context["change_url"] = reverse(f"admin:{app_label}_{model_name}_change",
                                        args=[self.object.id])
        context["delete_url"] = reverse(f"admin:{app_label}_{model_name}_delete",
                                        args=[self.object.id])
        return context
