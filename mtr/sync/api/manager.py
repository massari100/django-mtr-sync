from __future__ import unicode_literals

from collections import OrderedDict

from django.utils.six.moves import filterfalse
from django.db import models

from .exceptions import ProcessorAlreadyExists, ProcessorDoesNotExists
from .signals import filter_registered
from ..settings import IMPORT_PROCESSORS, MODEL_SETTINGS_NAME


class ModelManagerMixin(object):

    def get_model_field_by_name(self, model, name):
        """Return model field or custom method"""

        for field in model._meta.fields:
            if field.name == name:
                return field

        custom = getattr(model, name, None)
        if custom:
            custom._sync_custom_field = True

        return custom

    def model_settings(self, model):
        return getattr(model, MODEL_SETTINGS_NAME(), {})

    def models_list(self):
        mlist = filterfalse(
            lambda m: self.model_settings(m).get('ignore', False),
            models.get_models())
        return mlist

    def model_attributes(self, settings):
        """Return iterator of fields names by given mode_path"""

        model = self.model_class(settings)
        msettings = self.model_settings(model)

        exclude = msettings.get('exclude', [])
        fields = model._meta.get_all_field_names()
        fields += msettings.get('fields', [])

        fields = filterfalse(
            lambda f: f in exclude, fields)

        for name in fields:
            field = self.get_model_field_by_name(model, name)

            label = name
            custom_label = getattr(field, '_sync_custom_field', False)

            if custom_label:
                label = getattr(field, 'short_description', field.__name__)
            elif field:
                label = field.verbose_name

            yield (name, label.capitalize())

    def model_class(self, settings):
        """Return class for name in main_model"""

        for mmodel in self.models_list():
            if settings.main_model == '{}.{}'.format(
                    mmodel.__module__, mmodel.__name__):
                return mmodel

    def model_choices(self):
        """Return all registered django models as choices"""

        for model in self.models_list():
            yield (
                '{}.{}'.format(model.__module__, model.__name__),
                '{} | {}'.format(
                    model._meta.app_label.title(),
                    model._meta.verbose_name.title()))

    def queryset_choices(self):
        # TODO: return querysets

        return (
            ('', ''),
        )


class ProcessorManagerMixin(object):

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

    def has_processor(self, cls):
        """Check if processor already exists"""

        return True if self.processors.get(cls.__name__, False) else False

    def make_processor(self, settings, from_extension=False):
        """Create new processor instance if exists"""

        processor = None

        if from_extension:
            extension = settings.buffer_file.path.split('.')[-1]
            for pr in self.processors.values():
                if pr.file_format.strip('.') == extension:
                    processor = pr
                    settings.processor = processor.__name__
                    break
        else:
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
                self.process_value(
                    field, self.process_attribute(item, field), export=True)
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

        if settings.end_col:
            cols = processor.column(settings.end_col)
            if settings.start_col:
                cols -= processor.column(settings.start_col)
                cols += 1

            fields = fields[:cols]

        for row in data:
            model = {'attrs': {}, 'action': None}
            for index, field in enumerate(fields):
                col = processor.column(field.name) if field.name else index
                action, value = self.process_value(field, row[col])
                model['attrs'][field.attribute] = value
                model['action'] = action
            yield model


class Manager(ProcessorManagerMixin, ModelManagerMixin):

    """Manager for data processors"""

    def __init__(self):
        self.processors = OrderedDict()
        self.filters = dict()
        self.handlers = dict()

    def _register_dict(self, type_name, func_name, **kwargs):
        """Return decorator for adding functions as key, value to dict"""

        # TODO: preregister custom filters as user filters

        def decorator(func):
            items = getattr(self, '{}s'.format(type_name), None)
            new_name = func_name or func.__name__

            if items is not None:
                items[new_name] = func
                self._dict_registered(
                    type_name, new_name, func, items, **kwargs)

            return func

        return decorator

    def _dict_registered(self, type_name, func_name, func, items, **kwargs):
        """After registering decorator handler"""
        if type_name == 'filter':
            label = kwargs.get('label', None) or func_name
            description = kwargs.get('description', None)
            filter_registered.send(self.__class__, name=func_name,
                label=label, description=description)

    def register(self, type_name, item=None, name=None, **kwargs):
        """Decorator to append new processors, handlers"""

        func = None

        if type_name == 'processor':
            func = self._register_processor
        else:
            func = self._register_dict(type_name, name, **kwargs)

        if item:
            return func(item)
        else:
            return func

    def unregister(self, type_name, item=None):
        """Decorator to pop dict items"""

        if type_name == 'processor':
            self.processors.pop(item.__name__, None)
        else:
            items = getattr(self, '{}s'.format(type_name), None)
            if items is not None:
                items.pop(item, None)

        return item

    def process_attribute(self, model, field):
        attr = getattr(model, field.attribute)

        if hasattr(attr, '__call__'):
            attr = attr(self, field)

        return attr

    def process_filter(self, field, field_filter, value, process_action):
        """Method for processing filter from
        field filters registered in manager"""

        filter_func = self.filters.get(field_filter.name, None)
        if filter_func:
            value = filter_func(value, field, process_action)

        if isinstance(value, tuple):
            return value
        else:
            return None, value

    def process_value(self, field, value, export=False, action=None):
        process_action = 'export' if export else 'import'
        for field_filter in field.filters_queue:
            action, value = self.process_filter(
                field, field_filter, value, process_action)

        if export:
            return value
        else:
            return action, value

    def import_processors_modules(self):
        """Import modules within IMPORT_PROCESSORS paths"""

        for module in IMPORT_PROCESSORS():
            __import__(module)

manager = Manager()
manager.import_processors_modules()
