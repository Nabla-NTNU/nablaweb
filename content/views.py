# pylint: disable=C0111
"""
Mixin classes for views
"""
from django.core.urlresolvers import reverse
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


class ViewAddMixin:
    """
    Adds one view to the object each time the object is dispatched
    """

    def get_context_data(self, **kwargs):
        self.object.add_view()
        return super().get_context_data(**kwargs)


class PublishedMixin:
    """
    Fails to load unpublished objects.
    """

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        # pylint: disable=protected-access
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        perm = f"{app_label}.change_{model_name}"
        if self.get_object().is_published or user.has_perm(perm):
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("Ikke publisert")


def update_published_state(model):
    """
    Update the object with the new date.
    :param model: The model class to update
    """
    for m in model.objects.filter(published=False).iterator():
        if m.is_published:
            m.save()


class PublishedListMixin:
    """
    Excludes unpublished objects from the queryset.
    """

    def get_queryset(self):
        update_published_state(self.model)
        queryset = super().get_queryset()
        return queryset.exclude(published=False)
