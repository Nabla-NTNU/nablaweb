from django import template
from ..models import get_like_count

register = template.Library()


@register.simple_tag(takes_context=True)
def like_count(context):
    obj = context.get('object')
    model = obj.content_type.model
    count = get_like_count(obj.id, model)
    return str(count)
