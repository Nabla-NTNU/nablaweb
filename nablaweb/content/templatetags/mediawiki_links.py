# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
@stringfilter
def wikilinks(value):
    """Konverterer [[Bil]] til en lenke til wikisiden "Bil"."""
    rexp_pattern = re.compile("(\[\[(?P<page>.+?)\]\])")
    matches = rexp_pattern.finditer(value)
    
    new_value = value
    
    new_value = re.sub(rexp_pattern, '<a href="/wiki/\g<page>">\g<page></a>', value)
    
    return mark_safe(new_value)
