# -*- coding: utf-8 -*-


def get_primary_dir(request):
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
            'primary_dir_slashes': primary_dir_slashes}

