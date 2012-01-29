from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from datetime import datetime
import re
 
from django import template
register = template.Library()
 
@register.filter
def wordbreak (string, arg):
    search = '([^ ]{' + arg + '})'
    t = datetime.now()
    wbr = t.strftime("%A%d%B%Y%f") + 'wbr_here' + t.strftime("%A%d%B%Y%f")
    saferesult = conditional_escape(re.sub( search, '\\1' + wbr, string ))
    result = saferesult.replace(wbr,'&shy;')
    return mark_safe(result)
