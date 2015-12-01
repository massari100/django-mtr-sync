from decimal import Decimal

from django.utils.six import text_type
from django.utils.encoding import smart_text

from .manager import manager
from ..translation import gettext_lazy as _


@manager.register('converter', label=_('Decimal'))
def decimal(value, action):
    if value:
        if isinstance(value, text_type):
            value = value.replace(',', '.')
        return Decimal(value)
    else:
        return Decimal(0)


@manager.register('converter', label=_('String'))
def string(value, action):
    if value:
        return smart_text(value)
    else:
        return ''


@manager.register('converter', label=_('Coma separated list'))
def comalist(value, action):
    if action == 'export':
        if isinstance(value, list):
            return ','.join(map(lambda v: smart_text(v), value))
    else:
        if isinstance(value, text_type):
            return value.split(',')
    return [value]


@manager.register('converter', label=_('Boolean'))
def boolean(value, action):
    if value:
        return True
    else:
        return False


@manager.register('converter', label=_('File path'))
def filepath(value, action):
    if value:
        return value.path
    else:
        return value


@manager.register('converter', label=_('Integer'))
def integer(value, action):
    if value:
        return int(value)
    else:
        return value


@manager.register('converter', label=_('None'))
def none(value, action):
    return None
