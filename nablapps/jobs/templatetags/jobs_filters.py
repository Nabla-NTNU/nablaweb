from django import template

register = template.Library()


@register.filter
def commas_no(qset):
    """Formats a queryset as a list seperated by commas and "og" at the end."""
    string_list = list(map(str, qset))
    if len(string_list) < 2:
        return "".join(string_list)
    else:
        return ", ".join(string_list[:-1]) + " og " + string_list[-1]
