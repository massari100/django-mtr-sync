from ..translation import gettext_lazy as _


class ErrorChoicesMixin(object):
    IMPORT_DATA = 0
    UNDEFINED = 1

    STEP_CHOICES = (
        (IMPORT_DATA, _('import data')),
        (UNDEFINED, _('unexpected error'))
    )
