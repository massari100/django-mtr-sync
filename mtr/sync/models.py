from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .settings import FILE_PATH, strip_media_root
from .api import manager
from .api.helpers import model_attributes, model_choices, queryset_choices
from .api.signals import export_started, export_completed, \
    import_started, import_completed, error_raised, manager_registered, \
    receiver_for
from .api.exceptions import ErrorChoicesMixin


class PositionMixin(models.Model):
    position = models.PositiveIntegerField(
        _('mtr.sync:position'), null=True, blank=True)

    class Meta:
        abstract = True


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
        choices=model_choices())
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

    queryset = models.CharField(
        _('mtr.sync:queryset'), max_length=255, blank=True)

    def fields_with_processors(self):
        """Return iterator of fields with filters"""

        fields = self.fields.prefetch_related(
            'processor_params__processor_related') \
            .exclude(skip=True).all()
        for field in fields:
            field.ordered_processors = []

            for processor_param in field.processor_params.all():
                field.ordered_processors.append(
                    processor_param.processor_related)

            yield field

    def populate_from_buffer_file(self):
        # TODO: move set dimensions in processor open, create methods

        processor = manager.make_processor(self, from_extension=True)
        max_row, max_col = processor.open(self.buffer_file.path)
        processor.set_dimensions(0, 0, max_row, max_col)

        start_row, start_col = 0, 0

        index = 1
        while index < max_row:
            row = processor.read(index - 1)
            start_row = index

            for col_index, col in enumerate(row):
                if col:
                    start_col = col_index + 1
                    index = max_row
                    break
            index += 1

        self.start_row = start_row
        self.end_row = max_row

        self.start_col = start_col
        self.end_col = max_col

    def create_default_fields(self, exclude=None):
        """Create all fields for selected model"""

        fields = []

        if not exclude:
            exclude = []
        for name, label in model_attributes(self):
            if name not in exclude:
                fields.append(self.fields.create(
                    attribute=name, name=label))
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
class ValueProcessor(models.Model):

    """ValueProcessor data using internal template"""

    name = models.CharField(_('mtr.sync:name'), max_length=255)
    label = models.CharField(_('mtr.sync:label'), max_length=255)
    description = models.TextField(
        _('mtr.sync:description'), max_length=20000, null=True, blank=True)

    class Meta:
        verbose_name = _('mtr.sync:value processor')
        verbose_name_plural = _('mtr.sync:value processors')

        ordering = ('-id',)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Field(PositionMixin):

    """Data mapping field for Settings"""

    name = models.CharField(_('mtr.sync:name'), max_length=255, blank=True)
    attribute = models.CharField(_('mtr.sync:model attribute'), max_length=255)
    skip = models.BooleanField(_('mtr.sync:skip'), default=False)

    processors = models.ManyToManyField(
        ValueProcessor, through='ValueProcessorParams')

    settings = models.ForeignKey(
        Settings, verbose_name=_('mtr.sync:settings'), related_name='fields')

    def save(self, *args, **kwargs):
        if self.position is None:
            self.position = self.__class__.objects \
                .filter(settings=self.settings).count() + 1

        super(Field, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('mtr.sync:field')
        verbose_name_plural = _('mtr.sync:fields')

        ordering = ['position']

    def __str__(self):
        return self.name or self.attribute


@receiver(manager_registered)
@receiver_for('valueprocessor')
def create_valueprocessor(sender, **kwargs):
    ValueProcessor.objects.get_or_create(
        name=kwargs['func_name'], defaults={
            'label': kwargs.get('label', None) or kwargs['func_name'],
            'description': kwargs.get('description', None)
        })


@python_2_unicode_compatible
class ValueProcessorParams(PositionMixin):

    processor_related = models.ForeignKey(
        ValueProcessor, verbose_name=_('mtr.sync:filter'))
    field_related = models.ForeignKey(Field, related_name='processor_params')

    class Meta:
        verbose_name = _('mtr.sync:value processor')
        verbose_name_plural = _('mtr.sync:value processors')

        ordering = ['position']

    def save(self, *args, **kwargs):
        if self.position is None:
            self.position = self.__class__.objects \
                .filter(field_related=self.field_related).count() + 1

        super(ValueProcessorParams, self).save(*args, **kwargs)

    def __str__(self):
        return self.processor_related.label


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
        Settings, verbose_name=_('mtr.sync:settings'),
        related_name='reports', null=True, blank=True
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
    report = sender.report

    if sender.settings.id:
        report.settings = sender.settings

    report.completed_at = kwargs['date']
    report.buffer_file = kwargs['path']
    report.status = report.SUCCESS
    report.save()

    return report


@receiver(import_started)
def create_import_report(sender, **kwargs):
    return Report.import_objects.create(
        buffer_file=strip_media_root(kwargs['path']),
        action=Report.IMPORT)


@receiver(import_completed)
def save_import_report(sender, **kwargs):
    report = sender.report

    if sender.settings.id:
        report.settings = sender.settings

    report.completed_at = kwargs['date']
    report.status = report.SUCCESS
    report.save()

    return report


@python_2_unicode_compatible
class Error(PositionMixin, ErrorChoicesMixin):

    """Report errors with info about step where raised"""

    report = models.ForeignKey(Report, related_name='errors')

    message = models.TextField(_('mtr.sync:message'), max_length=10000)
    step = models.PositiveSmallIntegerField(
        _('mtr.sync:step'), choices=ErrorChoicesMixin.STEP_CHOICES,
        default=ErrorChoicesMixin.UNDEFINED)
    input_position = models.CharField(
        _('mtr.sync:input position'), max_length=10, blank=True)
    input_value = models.TextField(
        _('mtr.sync:input value'), max_length=60000, null=True, blank=True)

    class Meta:
        verbose_name = _('mtr.sync:error')
        verbose_name_plural = _('mtr.sync:errors')

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        if self.position is None:
            self.position = self.__class__.objects \
                .filter(report=self.report).count() + 1
        super(Error, self).save(*args, **kwargs)


@receiver(error_raised)
def create_error(sender, **kwargs):
    position = kwargs.get('position', '')
    value = kwargs.get('value', None)

    Error.objects.create(
        report=sender.report, message=kwargs['error'],
        step=kwargs['step'], input_position=position,
        input_value=repr(value) if value else None)
