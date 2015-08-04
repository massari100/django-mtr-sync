import os

from django.conf import settings

from ..utils.settings import getattr_with_prefix, strip_media_root
from ..utils.helpers import make_prefixed_gettext_lazy


gettext_lazy = make_prefixed_gettext_lazy('mtr.sync')


def get_buffer_file_path(instance, filename, absolute=False):
    """Generate file path for report"""

    action = getattr(instance, 'action', 1)
    action = 'import' if action else 'export'
    path = os.path.join(
        settings.MEDIA_ROOT, 'sync', action, filename.lower())

    if not absolute:
        path = strip_media_root(path)

    return path

SETTINGS = getattr_with_prefix('SYNC', 'SETTINGS', {
    # default processor
    'DEFAULT_PROCESSOR': 'XlsxProcessor',

    # register models at admin
    'REGISTER_IN_ADMIN': True,

    # path for report file
    'FILE_PATH': get_buffer_file_path,

    # additional dependensies for import and export to register
    'PROCESSORS': [
        'mtr.sync.lib.processors.xlsx',
        'mtr.sync.lib.processors.xls',
        'mtr.sync.lib.processors.ods',
        'mtr.sync.lib.processors.csv',
    ],
    'ACTIONS': ['mtr.sync.lib.actions'],
    'CONVERTERS': ['mtr.sync.lib.converters']
})
