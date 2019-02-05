import logging

from django.contrib.flatpages.models import FlatPage
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic.base import ContextMixin


class FlatPageMixin(ContextMixin):
    """
    Adds the content of a FlatPage object into the context of the view.
    """
    flatpages = []  # Should be a list of tuples of the form ("context_variable", "/flatpage/url")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        for context_name, url in self.flatpages:
            try:
                context[context_name] = FlatPage.objects.get(url=url)
            except FlatPage.DoesNotExist:
                logging.getLogger(__name__).warning("No flatpage at {}".format(url))
        return context


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
