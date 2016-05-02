from django.apps import AppConfig as BaseAppConfig

from .translation import gettext_lazy as _


class AppConfig(BaseAppConfig):
    name = 'mtr.sync'
    label = 'mtr_sync'
    verbose_name = _('Data sync')
