# from django.utils.six import text_type

from .manager import manager
from ..helpers import gettext_lazy as _


@manager.register('converter', label=_('Auto'))
def auto(value, model, field, mfields, action):
    """Auto convert values to field types in models"""

    # TODO: refactor to normal converter

    if action == 'export':
        if isinstance(value, list):
            return ','.join(map(lambda v: str(v), value))
    # else:
    #     if isinstance(value, text_type) and ',' in value:
    #         return value.split(',')

    return value
