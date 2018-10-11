import logging

from django.contrib.flatpages.models import FlatPage
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
