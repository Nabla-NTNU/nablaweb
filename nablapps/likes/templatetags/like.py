from django import template
from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template
from ..models import get_like_count, user_likes

register = template.Library()


@register.inclusion_tag('likes/like_button_include.html', takes_context=True)
def show_like_button_for(context, object):
    user = context['user']
    return {
        'object': object,
        'content_type': ContentType.objects.get_for_model(object.__class__),
        'liked': user_likes(object, user) if user.is_authenticated() else False,
        'like_count': get_like_count(object),
    }
