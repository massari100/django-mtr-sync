# import django

from django.utils.translation import gettext_lazy as _

# if django.get_version() >= '1.7':
#     from django.db.models.signals import post_syncdb as post_migrate
# else:
#     from django.db.models.signals import post_migrate

from .manager import manager


@manager.register('valueprocessor', label=_('mtr.sync:Auto'))
def auto(value, field, action):
    """Auto convert values to field types in models"""

    return action, value
