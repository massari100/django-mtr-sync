from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MtrSyncConfig(AppConfig):
    name = "mtr_sync"
    verbose_name = _("mtr_sync:app.verbose_name")
