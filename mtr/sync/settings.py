import os

import django

from django.conf import settings


# TODO: move to mtr.utils
def getattr_with_prefix(prefix, name, default):
    """Custom settings prefix for avoiding name colissions"""

    prefix = getattr(settings, '{}_SETTINGS_PREFIX'.format(prefix), prefix)

    default.update(getattr(settings, '{}_{}'.format(prefix, name), {}))

    return default


def strip_media_root(path):
    if path:
        return path.split(settings.MEDIA_ROOT.rstrip('/'))[1].lstrip('/')
    return path


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


if django.get_version() <= '1.7':
    SETTINGS.update({
        'PROCESSORS': [
            'mtr_sync.lib.processors.xlsx',
            'mtr_sync.lib.processors.xls',
            'mtr_sync.lib.processors.ods',
            'mtr_sync.lib.processors.csv',
        ],
        'ACTIONS': ['mtr_sync.lib.actions'],
        'CONVERTERS': ['mtr_sync.lib.converters']
    })
    SETTINGS.update(getattr_with_prefix('SYNC', 'SETTINGS', {}))
