from django import template

register = template.Library()

@register.filter
def commas_no(qset):
    final_str = ""
    for i in xrange(0,len(qset)):
        if (i == len(qset)-1):
            final_str += qset[i].__unicode__()
        elif (i == len(qset)-2):
            final_str += qset[i].__unicode__() + " og "
        else:
            final_str += qset[i].__unicode__() + ", "
    return final_str
