from django.utils.translation import gettext_lazy as _
from django.db import models

from .manager import manager


@manager.register('converter', label=_('mtr.sync:Auto'))
def auto(value, field, action):
    """Auto convert values to field types in models"""

    if isinstance(field, models.ManyToManyField):
        if isinstance(value, list):
            return ','.join(value)
        else:
            return value.split(',')

    return value
