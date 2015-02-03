import os

from django.conf import settings

# custom prefix for avoiding name colissions
PREFIX = getattr(settings, 'SYNC_SETTINGS_PREFIX', 'SYNC')


def getattr_with_prefix(name, default):
    """Shortcut for getting settings attribute with prefix"""

    return getattr(settings, '{}_{}'.format(PREFIX, name), default)


def get_buffer_file_path(instance, filename):
    """Generate file path for report"""

    return os.path.join(
        settings.MEDIA_ROOT, 'sync',
        instance.get_action_display().lower(), filename)

# used to generate custom file path
FILE_PATH = getattr_with_prefix('FILE_PATH', get_buffer_file_path)
