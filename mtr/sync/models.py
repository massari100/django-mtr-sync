from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.conf import settings as django_settings

from .settings import FILE_PATH, DEFAULT_PROCESSOR, strip_media_root
from .api import manager
from .api.helpers import model_attributes, model_choices
from .api.signals import export_started, export_completed, \
    import_started, import_completed, error_raised
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

    name = models.CharField(_('mtr.sync:name'), blank=True, max_length=100)

    start_col = models.CharField(
        _('mtr.sync:start column'), max_length=10, blank=True)
    start_row = models.PositiveIntegerField(
        _('mtr.sync:start row'), null=True, blank=True)

    end_col = models.CharField(
        _('mtr.sync:end column'), max_length=10, blank=True)
    end_row = models.PositiveIntegerField(
        _('mtr.sync:end row'), null=True, blank=True)

    model = models.CharField(
        _('mtr.sync:model'), max_length=255,
        choices=model_choices(), blank=True)

    created_at = models.DateTimeField(
        _('mtr.sync:created at'), auto_now_add=True)
    updated_at = models.DateTimeField(
        _('mtr.sync:updated at'), auto_now=True)

    processor = models.CharField(
        _('mtr.sync:format'), max_length=255,
        choices=manager.processor_choices(),
        default=DEFAULT_PROCESSOR())
    worksheet = models.CharField(
        _('mtr.sync:worksheet page'), max_length=255, blank=True)
    include_header = models.BooleanField(
        _('mtr.sync:include header'), default=True)

    filename = models.CharField(
        _('mtr.sync:custom filename'), max_length=255, blank=True)
    buffer_file = models.FileField(
        _('mtr.sync:file'), upload_to=FILE_PATH(), db_index=True, blank=True)

    dataset = models.CharField(
        _('mtr.sync:dataset'), max_length=255, blank=True,
        choices=manager.dataset_choices())
    data_action = models.CharField(
        _('mtr.sync:data action'), blank=True,
        max_length=255, choices=manager.action_choices())
    filter_dataset = models.BooleanField(
        _('mtr.sync:filter custom dataset'), default=True)
    filter_querystring = models.CharField(
        _('mtr.sync:querystring'), max_length=255, blank=True)

    language = models.CharField(
        _('mtr.sync:language'), blank=True,
        max_length=255, choices=django_settings.LANGUAGES)
    hide_translation_fields = models.BooleanField(
        _('mtr.sync:Hide translation prefixed fields'),
        default=True)

    create_fields = models.BooleanField(
        _('mtr.sync:Create settings for fields'), default=True)
    populate_from_file = models.BooleanField(
        _('mtr.sync:Populate settings from file'), default=False)
    run_after_save = models.BooleanField(
        _('mtr.sync:Start action after saving'), default=False)
    include_related = models.BooleanField(
        _('mtr.sync:Include related fields'), default=True)

    def fields_with_converters(self):
        """Return iterator of fields with converters"""

        fields = self.fields.exclude(skip=True)
        for field in fields:
            field.ordered_converters = []
            if field.converters:
                for converter in field.converters.split(','):
                    field.ordered_converters.append(
                        manager.get_or_raise('converter', converter))

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

    def create_default_fields(self, exclude=None, add_label=True):
        """Create all fields for selected model"""

        fields = []

        if not exclude:
            exclude = []

        if not self.model:
            return []

        for name, label in model_attributes(self):
            label = label if self.action != self.IMPORT and add_label else ''
            if name not in exclude:
                field = self.fields.create(
                    attribute=name, name=label, converters='auto')
                fields.append(field)

        return fields

    def run(self):
        """Run import or export task from celery"""

        from .tasks import export_data, import_data

        if self.action == self.EXPORT:
            export_data.apply_async(args=[{'id': self.id}])
        elif self.action == self.IMPORT:
            import_data.apply_async(args=[{'id': self.id}])

    def create_copy(self):
        fields = self.fields.all()
        contexts = self.contexts.all()

        self.id = None
        self.save()

        for field in fields:
            field.id = None
            field.settings_id = self.id
            field.save()

        for context in contexts:
            context.id = None
            context.settings_id = self.id
            context.save()

    class Meta:
        verbose_name = _('mtr.sync:settings')
        verbose_name_plural = _('mtr.sync:settings')

        ordering = ('-id',)

        app_label = 'mtr_sync'

    def __str__(self):
        return self.name or self.worksheet or str(self.id)


@python_2_unicode_compatible
class Sequence(models.Model):
    name = models.CharField(_('mtr.sync:name'), max_length=255)
    buffer_file = models.FileField(
        _('mtr.sync:file'), upload_to=FILE_PATH(), db_index=True, blank=True)

    settings = models.ManyToManyField(
        Settings, verbose_name=_('mtr.sync:settings'))

    class Meta:
        verbose_name = _('mtr.sync:sequence')
        verbose_name_plural = _('mtr.sync:sequences')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Field(PositionMixin):

    """Data mapping field for Settings"""

    # TODO: more filters and translations

    FILTER_CHOICES = (
        ('icontains', 'icontains'),
        ('contains', 'contains'),
        ('iexact', 'iexact'),
        ('exact', 'exact'),
        ('in', 'in'),
        ('gt', 'gt'),
        ('gte', 'gte'),
        ('lt', 'lt'),
        ('lte', 'lte'),
    )

    name = models.CharField(_('mtr.sync:name'), max_length=255, blank=True)
    attribute = models.CharField(
        _('mtr.sync:model attribute'), max_length=255)
    skip = models.BooleanField(_('mtr.sync:skip'), default=False)

    update = models.BooleanField(_('mtr.sync:update'), default=True)
    update_value = models.CharField(
        _('mtr.sync:value'), max_length=255, blank=True)
    find = models.BooleanField(_('mtr.sync:find'), default=False)
    find_filter = models.CharField(
        _('mtr.sync:filter type'), max_length=255, blank=True,
        choices=FILTER_CHOICES)

    converters = models.CharField(
        _('mtr.sync:converters'), max_length=255, blank=True)

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

        ordering = ('position',)

        app_label = 'mtr_sync'

    def __str__(self):
        return self.name or self.attribute


@python_2_unicode_compatible
class Context(models.Model):

    """Context for importing values in action"""

    name = models.CharField(_('mtr.sync:name'), max_length=255)
    cell = models.CharField(_('mtr.sync:cell'), max_length=1000, blank=True)
    value = models.CharField(_('mtr.sync:value'), max_length=1000, blank=True)

    settings = models.ForeignKey(
        Settings, verbose_name=_('mtr.sync:settings'),
        related_name='contexts', null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('mtr.sync:context')
        verbose_name_plural = _('mtr.sync:contexts')


@python_2_unicode_compatible
class Report(ActionsMixin):

    """Reports for imported and exported operations and link to files
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

        app_label = 'mtr_sync'

    def __str__(self):
        return '{} - {}'.format(self.started_at, self.get_status_display())

    def get_absolute_url(self):
        if self.buffer_file:
            return self.buffer_file.url


@receiver(export_started)
def create_export_report(sender, **kwargs):
    return Report.export_objects.create(
        action=Report.EXPORT, settings=sender.settings)


@receiver(export_completed)
def save_export_report(sender, **kwargs):
    report = sender.report

    report.completed_at = kwargs['date']
    report.buffer_file = kwargs['path']
    report.status = report.SUCCESS
    report.save()

    return report


@receiver(import_started)
def create_import_report(sender, **kwargs):
    return Report.import_objects.create(
        buffer_file=strip_media_root(kwargs['path']),
        settings=sender.settings,
        action=Report.IMPORT)


@receiver(import_completed)
def save_import_report(sender, **kwargs):
    report = sender.report

    report.completed_at = kwargs['date']
    report.save()

    return report


@python_2_unicode_compatible
class Message(PositionMixin, ErrorChoicesMixin):

    """Report errors with info about step where raised"""

    ERROR = 0
    INFO = 1

    MESSAGE_CHOICES = (
        (ERROR, _('mtr.sync:Error')),
        (INFO, _('mtr.sync:Info'))
    )

    report = models.ForeignKey(Report, related_name='errors')

    message = models.TextField(_('mtr.sync:message'), max_length=10000)
    step = models.PositiveSmallIntegerField(
        _('mtr.sync:step'), choices=ErrorChoicesMixin.STEP_CHOICES,
        default=ErrorChoicesMixin.UNDEFINED)
    input_position = models.CharField(
        _('mtr.sync:input position'), max_length=10, blank=True)
    input_value = models.TextField(
        _('mtr.sync:input value'), max_length=60000, null=True, blank=True)

    type = models.PositiveSmallIntegerField(
        _('mtr.sync:type'), choices=MESSAGE_CHOICES, default=ERROR)

    class Meta:
        verbose_name = _('mtr.sync:message')
        verbose_name_plural = _('mtr.sync:messages')

        ordering = ('position', )

        app_label = 'mtr_sync'

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        if self.position is None:
            self.position = self.__class__.objects \
                .filter(report=self.report).count() + 1
        super(Message, self).save(*args, **kwargs)


@receiver(error_raised)
def create_error(sender, **kwargs):
    position = kwargs.get('position', '')
    value = kwargs.get('value', None)

    Message.objects.create(
        report=sender.report, message=kwargs['error'],
        step=kwargs['step'], input_position=position,
        input_value=repr(value) if value else None)
