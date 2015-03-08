from django.utils.translation import gettext_lazy as _


class ErrorChoicesMixin(object):
    PREPARE_QUERYSET = 0
    PREPARE_DATA = 1
    SETUP_DIMENSIONS = 2
    OPEN_FILE = 3
    CREATE_FILE = 4
    WRITE_HEADER = 5
    WRITE_DATA = 6
    SAVE_FILE = 7
    READ_FILE = 8
    IMPORT_DATA = 9

    UNDEFINED = 10

    STEP_CHOICES = (
        (PREPARE_QUERYSET, _('mtr.sync:prepare queryset')),
        (PREPARE_DATA, _('mtr.sync:prepare data')),
        (SETUP_DIMENSIONS, _('mtr.sync:setup dimensions for file')),
        (OPEN_FILE, _('mtr.sync:open file')),
        (CREATE_FILE, _('mtr.sync:create file')),
        (WRITE_HEADER, _('mtr.sync:write header')),
        (WRITE_DATA, _('mtr.sync:write data')),
        (SAVE_FILE, _('mtr.sync:save file')),
        (READ_FILE, _('mtr.sync:read file')),
        (IMPORT_DATA, _('mtr.sync:import data')),
        (UNDEFINED, _('mtr.sync:unexpected error'))
    )


class ItemDoesNotRegistered(Exception):
    pass


class ItemAlreadyRegistered(Exception):
    pass


class NoIndexFound(Exception):
    pass
