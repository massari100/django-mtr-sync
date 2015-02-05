import os

from functools import wraps

from django.shortcuts import render

from .settings import THEME_PATH


def themed(template):
    """Changing template themes by setting THEME_PATH"""

    return os.path.join('mtr', 'sync', THEME_PATH(), template)


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

                return render(request, new_template, **decorator_kwargs)
            else:
                return response
        return wrapper

    return decorator
