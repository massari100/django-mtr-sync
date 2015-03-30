from django.utils.translation import gettext_lazy as _

from .manager import manager


@manager.register('valueprocessor', label=_('mtr.sync:Auto'))
def auto(value, field, action):
    """Auto convert values to field types in models"""

    return action, value
