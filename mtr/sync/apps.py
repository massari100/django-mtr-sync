from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MtrSyncConfig(AppConfig):
    name = 'mtr.sync'
    label = 'mtr_sync'
    verbose_name = _('mtr.sync:Data sync')
