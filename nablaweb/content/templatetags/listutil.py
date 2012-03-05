from django import template
register = template.Library()


@register.filter
def row_split(l, n):
    """
    Yields successive n-sized chunks of a list. Can be used to partition a list
    into rows, for HTML display.

    >>> l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> row_split(l, 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]

    Source: http://stackoverflow.com/questions/312443/
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]
