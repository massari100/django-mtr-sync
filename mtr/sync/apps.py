from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MtrSyncConfig(AppConfig):
    name = 'mtr.sync'
    label = 'mtrsync'
    verbose_name = _('mtr.sync:Data sync')

    def ready(self):
        # TODO: create fallback for django 1.6 or remove valueprocessors model

        __import__('mtr.sync.api.valueprocessors')
