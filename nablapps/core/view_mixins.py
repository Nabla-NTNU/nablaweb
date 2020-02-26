"""
Generic view mixins
"""
import logging

from django.contrib.flatpages.models import FlatPage
from django.urls import reverse
from django.views.generic.base import ContextMixin


class FlatPageMixin(ContextMixin):
    """
    Adds the content of a FlatPage object into the context of the view.
    """

    flatpages = (
        []
    )  # Should be a list of tuples of the form ("context_variable", "/flatpage/url")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        for context_name, url in self.flatpages:
            try:
                context[context_name] = FlatPage.objects.get(url=url)
            except FlatPage.DoesNotExist:
                logging.getLogger(__name__).warning("No flatpage at {}".format(url))
        return context


class AdminLinksMixin(ContextMixin):
    """
    Adds links to the admin page for an object to the context.

    Meant to be used together with DetailView.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["admin_links"] = self.get_admin_links()
        return context

    def get_admin_links(self):
        """
        Return list of dictionaries containing links.

        Override this to add more links.
        """
        # pylint: disable=protected-access
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return [
            {
                "name": "Endre",
                "glyphicon_symbol": "pencil",
                "url": reverse(
                    f"admin:{app_label}_{model_name}_change", args=[self.object.id]
                ),
            },
            {
                "name": "Slett",
                "glyphicon_symbol": "trash",
                "url": reverse(
                    f"admin:{app_label}_{model_name}_delete", args=[self.object.id]
                ),
            },
        ]
