# -*- coding: utf-8 -*-
from django.core.cache import cache
import urllib
import json

def primary_dir(request):
    """Adds the primary URL path to context.

    For example, if the user is visting http://nabla.no/batman/cakes,
    primary_dir would be "batman".

    """
    primary_dir = request.path.split('/')[1]
    if primary_dir:
        primary_dir_slashes = '/' + primary_dir + '/'
    else:
        primary_dir_slashes = '/'
    return {'primary_dir': primary_dir,
            'primary_dir_slashes': primary_dir_slashes }


def xkcd(request):
    """Gets info about the newest xkcd-comic."""

    xkcd_data = cache.get("xkcd_data")
    if not xkcd_data:
        try:
            uopen = urllib.urlopen('http://xkcd.com/info.0.json')
            json_string = uopen.read()
            xkcd_data = json.loads(json_string)
            cache.set('xkcd_data', xkcd_data, 36000)
        except:
            return {}

    # Stoler på at xkcd ikke har noe tull(javascript ol.)  her, men burde egentlig sikres på
    # en eller annen måte.
    context = {}
    keys = ['safe_title','alt','img','title']
    for key in keys:
        context['xkcd_'+key] = xkcd_data[key]
    return context

