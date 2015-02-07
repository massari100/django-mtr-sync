from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.translation import gettext_lazy as _

from .settings import FILE_PATH


class ExportManager(models.Manager):
    """Shortcut for export queryset"""

    def get_queryset(self):
        return super(ExportManager, self).get_queryset() \
            .filter(action=self.model.EXPORT)


class ImportManager(models.Manager):
    """Shortcut for import queryset"""

    def get_queryset(self):
        return super(ImportManager, self).get_queryset() \
            .filter(action=self.model.IMPORT)


class RunningManager(models.Manager):
    """Shortcut for running log entry queryset"""

    def get_queryset(self):
        return super(RunningManager, self).get_queryset() \
            .filter(status=self.model.RUNNING)


@python_2_unicode_compatible
class LogEntry(models.Model):
    """Stores reports about imported and exported operations and link to files
    """

    ERROR = 0
    RUNNING = 1
    SUCCESS = 2

    STATUS_CHOICES = (
        (ERROR, _('mtr.sync:Error')),
        (RUNNING, _('mtr.sync:Running')),
        (SUCCESS, _('mtr.sync:Success'))
    )

    EXPORT = 0
    IMPORT = 1

    ACTION_CHOICES = (
        (EXPORT, _('mtr.sync:Export')),
        (IMPORT, _('mtr.sync:Import'))
    )

    buffer_file = models.FileField(
        _('mtr.sync:file'), upload_to=FILE_PATH())
    status = models.PositiveSmallIntegerField(
        _('mtr.sync:status'), choices=STATUS_CHOICES, default=RUNNING)
    action = models.PositiveSmallIntegerField(
        _('mtr.sync:action'), choices=ACTION_CHOICES, db_index=True)

    started_at = models.DateTimeField(
        _('mtr.sync:started at'), auto_now_add=True)
    completed_at = models.DateTimeField(
        _('mtr.sync:completed at'), null=True, blank=True)
    updated_at = models.DateTimeField(
        _('mtr.sync:updated at'), auto_now=True)

    export_objects = ExportManager()
    import_objects = ImportManager()
    running_objects = RunningManager()

    class Meta:
        verbose_name = _('mtr.sync:log entry')
        verbose_name_plural = _('mtr.sync:log entries')

        get_latest_by = '-started_at'

    def __str__(self):
        return '{} - {}'.format(self.started_at, self.get_status_display())

    def get_absolute_url(self):
        return self.buffer_file.url
