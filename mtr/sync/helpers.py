import os

from functools import wraps

import django

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as ugettext_lazy_original


def gettext_prefix(string, context=None):
    """Adding prefix for gettext message string"""

    return '{}:{}'.format('mtr.sync' or context, string)


def gettext_lazy(string, context=None):
    """Lazy gettext shortcut"""

    return ugettext_lazy_original(gettext_prefix(string, context))


def themed(template, version_subdirectory=False):
    """Changing template themes by setting THEME_PATH and django version"""

    path = 'default'

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
