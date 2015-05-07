import os

from functools import wraps

import django

from django.shortcuts import render

from .settings import THEME_PATH


def themed(template, version_subdirectory=False):
    """Changing template themes by setting THEME_PATH and django version"""

    path = THEME_PATH()

    if version_subdirectory:
        path = os.path.join(path, django.get_version()[:3])

    return os.path.join('mtr', 'sync', path, template)


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
                if decorator_kwargs.pop('themed', True):
                    new_template = themed(template)

                return render(
                    request, new_template,
                    response, **decorator_kwargs)
            else:
                return response
        return wrapper

    return decorator


def make_from_params(cls, params):
    """Create or fetch Model instance from params"""

    instance_id = params.get('id', False)
    if instance_id:
        instance = cls.objects.get(pk=instance_id)
    else:
        instance = cls(**params)

    return instance
