from django import template

register = template.Library()

@register.filter
def commas(tuple):
    list = [ ]
    for i in tuple:
        list.append(i.studieretning)
    length = len(list)
    string = ""
    if length == 1:
        return list[0]
    else:
        for i in range(length):
            if 0 < i < length-1:
                string += ', ' + list[i]
            elif i == 0:
                string += list[i]
            else:
                string += ' og ' + list[i]
        return string
