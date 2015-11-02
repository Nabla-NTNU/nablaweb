from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from ..core.markdown import content_markdown

register = template.Library()


@register.filter
@stringfilter
def markdown(value, option=""):
    return mark_safe(content_markdown(value))
