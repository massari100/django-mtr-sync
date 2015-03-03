from functools import wraps

from django.dispatch import Signal

export_started = Signal(['processor'])
export_completed = Signal(['report', 'completed_at', 'path'])

import_started = Signal([])
import_completed = Signal(['report', 'completed_at'])

error_raised = Signal(['exception'])
manager_registered = Signal(
    ['type_name', 'func_name', 'func', 'manager', '**kwargs'])


def receiver_for(name):
    """Decorator for filtering signals only for used names"""

    # outer decorator
    def decorator(f):

        # inner decorator
        @wraps(f)
        def wrapper(sender, **kwargs):
            if kwargs['type_name'] == name:
                return f(sender, **kwargs)

        return wrapper

    return decorator
