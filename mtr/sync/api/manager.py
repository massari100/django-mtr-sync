from __future__ import unicode_literals

from collections import OrderedDict
from django.utils.six.moves import filterfalse
from django.db import models

from .exceptions import ProcessorAlreadyExists, ProcessorDoesNotExists
from ..settings import IMPORT_PROCESSORS, MODEL_SETTINGS_NAME


class Manager(object):
    """Manager for data processors"""

    def __init__(self):
        self.processors = OrderedDict()

    def model_settings(self, model):
        return getattr(model, MODEL_SETTINGS_NAME(), {})

    def models_list(self):
        mlist = filterfalse(
            lambda m: self.model_settings(m).get('ignore', False),
            models.get_models())
        return mlist

    def get_field_by_name(self, model, name):
        for field in model._meta.fields:
            if field.name == name:
                return field

    def model_attributes(self, settings):
        """Return iterator of fields names by given mode_path"""

        model = self.model_class(settings)
        settings = self.model_settings(model)

        exclude = settings.get('exclude', [])
        fields = filterfalse(
            lambda f: f in exclude, model._meta.get_all_field_names())

        for name in fields:
            field = self.get_field_by_name(model, name)

            label = name
            if field:
                label = field.verbose_name

            yield (name, label.capitalize())

    def model_class(self, settings):
        """Return class for name in main_model"""

        # TODO: use module

        for mmodel in self.models_list():
            if settings.main_model.split('.')[-1] == mmodel.__name__:
                return mmodel

    def model_choices(self):
        """Return all registered django models as choices"""

        for model in self.models_list():
            # TODO: replace app name from app settings

            yield (
                '{}.{}'.format(model.__module__, model.__name__),
                '{} | {}'.format(
                    model._meta.app_label.title(),
                    model._meta.verbose_name.title()))

    def processor_choices(self):
        """Return all registered processors"""

        for processor in self.processors.values():
            yield (
                processor.__name__,
                '{} | {}'.format(
                    processor.file_format,
                    processor.file_description))

    def _register_processor(self, cls):
        if self.has_processor(cls):
            raise ProcessorAlreadyExists(
                'Processor {} already exists'.format(cls.__name__))
        self.processors[cls.__name__] = cls

        if cls.position:
            self.processors = OrderedDict(
                sorted(self.processors.items(), key=lambda p: p[1].position))

        return cls

    def register(self, name, cls=None):
        """Decorator to append new processors, handlers"""

        func = None

        if name == 'processor':
            func = self._register_processor

        if cls:
            return func(cls)
        else:
            return func

    def unregister(self, name, cls):
        """Decorator to pop processor"""

        if name == 'processor':
            self.processors.pop(cls.__name__, None)

        return cls

    def has_processor(self, cls):
        """Check if processor already exists"""

        return True if self.processors.get(cls.__name__, False) else False

    def make_processor(self, settings):
        """Create new processor instance if exists"""

        processor = self.processors.get(settings.processor, None)

        if processor is None:
            raise ProcessorDoesNotExists(
                'Processor {} does not exists'.format(settings.processor))

        return processor(settings, self)

    def export_data(self, settings, data=None):
        """Export data to file if no data passed,
        create queryset it from settings"""

        processor = self.make_processor(settings)

        if data is None:
            queryset = self.prepare_export_queryset(settings)
            data = self.prepare_export_data(processor, queryset)

        return processor.export_data(data)

    def prepare_export_queryset(self, settings):
        current_model = self.model_class(settings)
        model_settings = self.model_settings(current_model)
        queryset = model_settings.get('queryset', None)

        # TODO: add aditional fields or methods

        # TODO: automatic select_related, prefetch_related

        if queryset:
            queryset = queryset(settings)
        else:
            queryset = current_model.objects.all()

        return queryset

    def prepare_export_data(self, processor, queryset):
        """Prepare data using filters from settings
        and return data with dimensions"""

        settings = processor.settings
        fields = list(settings.fields_with_filters())

        if settings.end_row:
            rows = settings.end_row
            if settings.start_row:
                rows -= settings.start_row
                rows += 1

            queryset = queryset[:rows]

        if settings.end_col:
            cols = processor.column(settings.end_col)
            if settings.start_col:
                cols -= processor.column(settings.start_col)
                cols += 1

            fields = fields[:cols]

        data = {
            'rows': queryset.count(),
            'cols': len(fields),
            'fields': fields,
            'items': (
                self.process_value(field, getattr(item, field.attribute))
                for item in queryset
                for field in fields
            )
        }

        return data

    def import_data(self, settings, path=None):
        """Import data to database"""

        processor = self.make_processor(settings)
        model = self.model_class(settings)

        return processor.import_data(model, path)

    def prepare_import_data(self, processor, data):
        """Prepare data using filters from settings and return iterator"""

        settings = processor.settings
        fields = list(settings.fields_with_filters())

        for row in data:
            attrs = {}
            for index, field in enumerate(fields):
                col = processor.column(field.name) if field.name else index
                value = self.process_value(field, row[col])
                attrs[field.attribute] = value
            yield attrs

    def process_value(self, field, value):
        # TODO: process by all filters
        # TODO: manual setted filters

        return value

    def import_processors_modules(self):
        """Import modules within IMPORT_PROCESSORS paths"""

        for module in IMPORT_PROCESSORS():
            __import__(module)

manager = Manager()
manager.import_processors_modules()
