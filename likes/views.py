from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST

from .models import toggle_like, get_like_count
from .utils import get_object, LikeException


@require_POST
@login_required
def toggle_like_view(request):
    try:
        object = get_object(
            request.POST['contenttypeId'],
            request.POST['objectId'])
    except KeyError:
        return HttpResponseBadRequest("Missing parameters for like")
    except LikeException as e:
        return HttpResponseBadRequest(e.message)

    is_liked = toggle_like(instance=object, user=request.user)

    count = get_like_count(object)
    return JsonResponse({'count': count, 'liked': is_liked })
