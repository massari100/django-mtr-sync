from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .settings import FILE_PATH
from .api import manager
from .api.signals import export_started, export_completed, \
    import_started, import_completed


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
    """Shortcut for running Report entry queryset"""

    def get_queryset(self):
        return super(RunningManager, self).get_queryset() \
            .filter(status=self.model.RUNNING)


class ActionsMixin(models.Model):
    """Action choices mixin"""

    EXPORT = 0
    IMPORT = 1

    ACTION_CHOICES = (
        (EXPORT, _('mtr.actions:Export')),
        (IMPORT, _('mtr.actions:Import'))
    )

    action = models.PositiveSmallIntegerField(
        _('mtr.sync:action'), choices=ACTION_CHOICES, db_index=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Settings(ActionsMixin):
    """Settings for imported and exported files"""

    name = models.CharField(_('mtr.sync:name'), max_length=100)

    start_col = models.CharField(
        _('mtr.sync:start column'), max_length=10, blank=True)
    start_row = models.PositiveIntegerField(
        _('mtr.sync:start row'), null=True, blank=True)

    end_col = models.CharField(
        _('mtr.sync:end column'), max_length=10, blank=True)
    end_row = models.PositiveIntegerField(
        _('mtr.sync:end row'), null=True, blank=True)

    main_model = models.CharField(
        _('mtr.sync:main model'), max_length=255,
        choices=manager.model_choices())
    main_model_id = models.PositiveIntegerField(
        _('mtr.sync:main model object'), null=True, blank=True)

    created_at = models.DateTimeField(
        _('mtr.sync:created at'), auto_now_add=True)
    updated_at = models.DateTimeField(
        _('mtr.sync:updated at'), auto_now=True)

    processor = models.CharField(
        _('mtr.sync:format'), max_length=255,
        choices=manager.processor_choices())
    worksheet = models.CharField(
        _('mtr.sync:worksheet page'), max_length=255, blank=True)

    include_header = models.BooleanField(
        _('mtr.sync:include header'), default=True)

    filename = models.CharField(
        _('mtr.sync:custom filename'), max_length=255, blank=True)

    buffer_file = models.FileField(
        _('mtr.sync:file'), upload_to=FILE_PATH(), db_index=True, blank=True)

    def fields_with_filters(self):
        """Return iterator of fields with filters"""

        fields = self.fields.prefetch_related(
            'filter_params__filter_related').exclude(skip=True).all()
        for field in fields:
            field.filters_queue = []

            for filter_param in field.filter_params.all():
                field.filters_queue.append(filter_param.filter_related)

            yield field

    def create_default_fields(self):
        """Create all fields for selected model"""

        fields = []

        for name, label in manager.model_attributes(self):
            fields.append(self.fields.create(attribute=name))

        return fields

    def run(self):
        """Run import or export task from celery"""

        from .tasks import export_data, import_data

        if self.action == self.EXPORT:
            export_data.apply_async(args=[{'id': self.id}])
        elif self.action == self.IMPORT:
            import_data.apply_async(args=[{'id': self.id}])

    class Meta:
        verbose_name = _('mtr.sync:settings')
        verbose_name_plural = _('mtr.sync:settings')

        ordering = ('-id',)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Filter(models.Model):
    """Filter data using internal template"""

    name = models.CharField(_('mtr.sync:name'), max_length=255)
    description = models.TextField(
        _('mtr.sync:description'), max_length=20000, null=True, blank=True)
    template = models.TextField(_('mtr.sync:template'), max_length=50000)

    class Meta:
        verbose_name = _('mtr.sync:filter')
        verbose_name_plural = _('mtr.sync:filters')

        ordering = ('-id',)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Field(models.Model):
    """Data mapping field for Settings"""

    order = models.PositiveIntegerField(
        _('mtr.sync:order'), null=True, blank=True)

    name = models.CharField(_('mtr.sync:name'), max_length=255, blank=True)
    attribute = models.CharField(_('mtr.sync:model attribute'), max_length=255)
    skip = models.BooleanField(_('mtr.sync:skip'), default=False)

    filters = models.ManyToManyField(Filter, through='FilterParams')

    settings = models.ForeignKey(
        Settings, verbose_name=_('mtr.sync:settings'), related_name='fields')

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = self.__class__.objects \
                .filter(settings=self.settings).count() + 1

        super(Field, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('mtr.sync:field')
        verbose_name_plural = _('mtr.sync:fields')

        ordering = ['order']

    def __str__(self):
        return self.name or self.attribute


@python_2_unicode_compatible
class FilterParams(models.Model):
    order = models.PositiveIntegerField(
        _('mtr.sync:order'), null=True, blank=True)

    filter_related = models.ForeignKey(
        Filter, verbose_name=_('mtr.sync:filter'))
    field_related = models.ForeignKey(Field, related_name='filter_params')

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = self.__class__.objects \
                .filter(field_related=self.field_related).count() + 1

        super(FilterParams, self).save(*args, **kwargs)

    def __str__(self):
        return self.filter_related.name

    class Meta:
        verbose_name = _('mtr.sync:filter')
        verbose_name_plural = _('mtr.sync:filters')

        ordering = ['order']


@python_2_unicode_compatible
class Report(ActionsMixin):
    """Reports about imported and exported operations and link to files
    """

    ERROR = 0
    RUNNING = 1
    SUCCESS = 2

    STATUS_CHOICES = (
        (ERROR, _('mtr.sync:Error')),
        (RUNNING, _('mtr.sync:Running')),
        (SUCCESS, _('mtr.sync:Success'))
    )

    buffer_file = models.FileField(
        _('mtr.sync:file'), upload_to=FILE_PATH(), db_index=True, blank=True)
    status = models.PositiveSmallIntegerField(
        _('mtr.sync:status'), choices=STATUS_CHOICES, default=RUNNING)

    started_at = models.DateTimeField(
        _('mtr.sync:started at'), auto_now_add=True)
    completed_at = models.DateTimeField(
        _('mtr.sync:completed at'), null=True, blank=True)
    updated_at = models.DateTimeField(
        _('mtr.sync:updated at'), auto_now=True)

    settings = models.ForeignKey(
        Settings, verbose_name=_('mtr.sync:used settings'),
        null=True, blank=True, related_name='reports'
    )

    objects = models.Manager()
    export_objects = ExportManager()
    import_objects = ImportManager()
    running_objects = RunningManager()

    class Meta:
        verbose_name = _('mtr.sync:report')
        verbose_name_plural = _('mtr.sync:reports')

        ordering = ('-id',)

    def __str__(self):
        return '{} - {}'.format(self.started_at, self.get_status_display())

    def get_absolute_url(self):
        if self.buffer_file:
            return self.buffer_file.url


@receiver(export_started)
def create_export_report(sender, **kwargs):
    return Report.export_objects.create(action=Report.EXPORT)


@receiver(export_completed)
def save_export_report(sender, **kwargs):
    report = kwargs['report']
    report.completed_at = kwargs['date']
    report.buffer_file = kwargs['path']
    report.status = report.SUCCESS
    report.save()

    return report


@receiver(import_started)
def create_import_report(sender, **kwargs):
    return Report.import_objects.create(
        buffer_file=kwargs['path'], action=Report.IMPORT)


@receiver(import_completed)
def save_import_report(sender, **kwargs):
    report = kwargs['report']
    report.completed_at = kwargs['date']
    report.status = report.SUCCESS
    report.save()

    return report
