from __future__ import unicode_literals

import django

if django.get_version() >= '1.7':
    from django.apps import AppConfig
    from django.utils.translation import gettext_lazy as _

    class MtrSyncConfig(AppConfig):
        name = 'mtr.sync'
        label = 'mtrsync'
        verbose_name = _('mtr.sync:Data sync')
