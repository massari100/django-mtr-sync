import os
import collections

from functools import wraps

import django

from django.shortcuts import render

from .settings import THEMES


def themed(template, version_subdirectory=False):
    """Changing template themes by setting THEME_PATH and django version"""

    path = os.path.join(THEMES['DIR'], THEMES['THEME'])

    if version_subdirectory:
        path = os.path.join(path, django.get_version()[:3])

    return os.path.join(path, template)


def render_to(template, *args, **kwargs):
    """Shortuct for rendering templates,
    creates functions that returns decorator for view"""

    decorator_kwargs = kwargs

    # outer decorator
    def decorator(f):

        # inner decorator
        @wraps(f)
        def wrapper(request, *args, **kwargs):
            response = f(request, *args, **kwargs)
            if isinstance(response, dict):
                new_template = template
                if decorator_kwargs.pop('themed', THEMES['USE_IN_RENDER']):
                    new_template = themed(template)

                return render(
                    request, new_template,
                    response, **decorator_kwargs)
            else:
                return response
        return wrapper

    return decorator


def make_prefixed_themed(prefix):
    """Shortcut for prefixing template dir path"""
    def inner(template, version_subdirectory=False):
        return themed(
            os.path.join(prefix, template),
            version_subdirectory=version_subdirectory)
    return inner


def make_prefixed_render_to(prefix):
    """Shortcut for prefixing template dir render"""

    def inner(template, *args, **kwargs):
        return render_to(
            os.path.join(prefix, template), *args, **kwargs)
    return inner


def chunks(l, n):
    """Chunk list"""

    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


def update_nested_dict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = update_nested_dict(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def make_from_params(model, params):
    if params.get('id', None):
        return model.objects.get(id=params['id'])
    return model(**params)
