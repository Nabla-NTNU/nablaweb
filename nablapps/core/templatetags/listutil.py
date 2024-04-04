"""
Templatetags for dealing with python lists in django template
"""

from django import template

register = template.Library()


@register.filter
def row_split(items, n):
    """
    Yields successive n-sized chunks of a list. Can be used to partition a list
    into rows, for HTML display.

    >>> items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> row_split(items, 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]

    Source: http://stackoverflow.com/questions/312443/
    """
    for i in range(0, len(items), n):
        yield items[i : i + n]
