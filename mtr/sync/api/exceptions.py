from ..helpers import gettext_lazy as _


class ErrorChoicesMixin(object):
    PREPARE_QUERYSET = 0
    PREPARE_DATA = 1
    OPEN_FILE = 3
    CREATE_FILE = 4
    WRITE_HEADER = 5
    WRITE_DATA = 6
    SAVE_FILE = 7
    READ_FILE = 8
    IMPORT_DATA = 9

    UNDEFINED = 10

    STEP_CHOICES = (
        (PREPARE_QUERYSET, _('prepare queryset')),
        (PREPARE_DATA, _('prepare data')),
        (OPEN_FILE, _('open file')),
        (CREATE_FILE, _('create file')),
        (WRITE_HEADER, _('write header')),
        (WRITE_DATA, _('write data')),
        (SAVE_FILE, _('save file')),
        (READ_FILE, _('read file')),
        (IMPORT_DATA, _('import data')),
        (UNDEFINED, _('unexpected error'))
    )


class ItemDoesNotRegistered(Exception):
    pass


class ItemAlreadyRegistered(Exception):
    pass
