from django.utils.translation import gettext_lazy as _
from django.utils.six import text_type

from .manager import manager


@manager.register('converter', label=_('mtr.sync:Auto'))
def auto(value, model, field, mfields, action):
    """Auto convert values to field types in models"""

    if action == 'export':
        if isinstance(value, list):
            return ','.join(map(lambda v: str(v), value))
    else:
        if isinstance(value, text_type) and ',' in value:
            return value.split(',')

    return value
