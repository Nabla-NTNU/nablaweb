from postmarkup.postmarkup import render_bbcode
from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def bbcode(value):
    return mark_safe(render_bbcode(value))
