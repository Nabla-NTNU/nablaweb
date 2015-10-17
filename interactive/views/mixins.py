from django.http import HttpResponseForbidden


class ObjectOwnerMixin(object):
    """
    Stops the view from being executed for users other than the owner
    """

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        obj = self.get_object()
        if obj.user == user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
