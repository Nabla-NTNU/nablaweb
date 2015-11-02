from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden


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


class PublishedMixin(object):
    """
    Fails to load unpublished objects.
    """

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        perm = "content.change_{}".format(self.model.__name__)
        if self.get_object().is_published or user.has_perm(perm):
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("Ikke publisert")


def update_published_state(model):
    """
    Update the object with the new date.
    :param model: The model class to update
    """
    for m in model.objects.all():
        m.save()


class PublishedListMixin(object):
    """
    Excludes unpublished objects from the queryset.
    """

    def get_queryset(self):
        update_published_state(self.model)
        queryset = super().get_queryset()
        return queryset.exclude(published=False)

