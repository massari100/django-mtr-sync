from __future__ import unicode_literals

import os
import traceback

from collections import OrderedDict

from django.utils.six.moves import filterfalse
from django.utils.translation import activate
from django.utils import timezone
from django.db import transaction, Error
from django.http import QueryDict
from django.core.exceptions import ValidationError
from django.contrib.admin.views.main import IGNORED_PARAMS

from .exceptions import ItemAlreadyRegistered, ItemDoesNotRegistered, \
    ErrorChoicesMixin
from .signals import export_started, export_completed, \
    import_started, import_completed, error_raised
from .helpers import make_model_class, model_settings, \
    process_attribute, model_fields, cell_value
from ..settings import SETTINGS


class Worker(object):

    def create_export_path(self):
        # TODO: refactor filepath

        filename = '{}{}'.format(
            self.settings.filename or str(self.report.id), self.file_format)
        path = SETTINGS['FILE_PATH'](self.report, '', absolute=True)
        if not os.path.exists(path):
            os.makedirs(path)

        return filename, os.path.join(path, filename)

    def write_header(self, data):
        if self.settings.include_header and data['fields']:
            header_data = list(map(
                lambda f: f.name or f.attribute,
                data['fields']))

            self.write(self.start['row'], header_data)

    def export_data(self, data):
        """Export data from queryset to file and return path"""

        # send signal to create report
        for response in export_started.send(self):
            self.report = response[1]

        self.set_dimensions(0, data['rows'], data['cols'])
        filename, path = self.create_export_path()
        self.create(path)

        # write header
        self.write_header(data)

        # write data
        data = data['items']

        for row in self.rows:
            row_data = []

            for col in self.cells:
                row_data.append(next(data))

            self.write(row, row_data)

        self.save()

        # send signal to save report
        for response in export_completed.send(
                self, date=timezone.now(),
                path=SETTINGS['FILE_PATH'](self.report, filename)):
            self.report = response[1]

        return self.report

    def _prepare_fk_attrs(self, related_attrs, key, _model):
        key_model, key_attr = key.split('|_fk_|')

        attrs = related_attrs.get(key_model, {})
        attrs[key_attr] = _model[key]
        related_attrs[key_model] = attrs

        return related_attrs

    def _prepare_mtm_attrs(self, related_attrs, key, _model):
        key_model, key_attr = key.split('|_m_|')

        value = _model[key]

        attrs = related_attrs.get(key_model, {})
        attrs[key_attr] = value
        related_attrs[key_model] = attrs

        return related_attrs

    def prepare_attrs(self, _model):
        model_attrs = {}
        related_attrs = {}

        for key in _model.keys():
            if '|_fk_|' in key:
                related_attrs = self._prepare_fk_attrs(
                    related_attrs, key, _model)
            elif '|_m_|' in key:
                related_attrs = self._prepare_mtm_attrs(
                    related_attrs, key, _model)
            else:
                model_attrs[key] = _model[key]

        return model_attrs, related_attrs

    def import_data(self, model, path=None):
        """Import data to model and return errors if exists"""

        if self.settings.buffer_file:
            path = self.settings.buffer_file.path

        # send signal to create report
        for response in import_started.send(self, path=path):
            self.report = response[1]
        self.report.status = self.report.SUCCESS

        data = self.manager.prepare_import_data(self, model)
        params = self.manager.filter_dataset(self.settings) or {}
        action = self.manager.get_or_raise('action', self.settings.data_action)
        context = self.manager.prepare_context(self.settings, path)
        context = self.manager.prepare_handlers('before', self, model, context)

        if path:
            self.open(path)

        use_transaction = getattr(action, 'use_transaction', False)
        if use_transaction:
            action = transaction.atomic(action)

        for row, _model in data['items']:
            model_attrs, related_attrs = self.prepare_attrs(_model)
            model_attrs.update(**params)

            kwargs = dict(
                processor=self, path=path, fields=data['fields'],
                params=params, raw_attrs=_model,
                mfields=data['mfields'],
            )

            if use_transaction:
                sid = transaction.savepoint()

            try:
                context = action(
                    model, model_attrs, related_attrs, context, **kwargs)
            except (Error, ValueError, ValidationError,
                    AttributeError, TypeError, IndexError):
                if use_transaction:
                    transaction.savepoint_rollback(sid)

                error_message = traceback.format_exc()

                value = {
                    'model_attrs': model_attrs,
                    'related_attrs': related_attrs
                }

                error_raised.send(
                    self,
                    error=error_message,
                    position=row,
                    value=value,
                    step=ErrorChoicesMixin.IMPORT_DATA)
                self.report.status = self.report.ERROR

                context.update(kwargs)
                context['error_message'] = error_message

                self.manager.prepare_handlers(
                    'error', self, model, context)

        self.manager.prepare_handlers('after', self, model, context)

        # send signal to save report
        for response in import_completed.send(
                self, date=timezone.now()):
            self.report = response[1]

        return self.report


class ProcessorManagerMixin(object):

    def convert_value(self, value, field, export=False, action=None):
        """Process value with filters and actions"""

        convert_action = 'export' if export else 'import'

        for convert_func in field.ordered_converters:
            value = convert_func(value, convert_action)

        return value

    def processor_choices(self):
        """Return all registered processors"""

        for name, processor in self.processors.items():
            yield (
                name,
                '{} | {}'.format(
                    processor.file_format,
                    processor.file_description))

    def dataset_choices(self):
        """Return all registered data sources"""

        for name, dataset in self.datasets.items():
            yield(name, getattr(dataset, 'label', dataset.__name__))

    def action_choices(self):
        """Return all registered actions"""

        for name, action in self.actions.items():
            yield(name, getattr(action, 'label', action.__name__))

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

        processor = self.get_or_raise('processor', settings.processor)

        return processor(settings, self)

    def export_data(self, settings, data=None):
        """Export data to file if no data passed,
        create queryset it from settings"""

        if settings.language:
            activate(settings.language)

        processor = self.make_processor(settings)

        if data is None:
            queryset = self.prepare_export_dataset(settings)
            data = self.prepare_export_data(processor, queryset)

        return processor.export_data(data)

    def export_data_inline(self, **settings):
        """Export data from inline settings, without creating instances"""

        fields = settings.get('fields', [])

        if fields is None:
            pass

    def import_data_inline(self, **settings):
        """Import data from inline settings, without creating instances"""

        fields = settings.get('fields', [])

        if fields is None:
            pass

    def filter_dataset(self, settings, dataset=None):
        if settings.filter_dataset and settings.filter_querystring:
            params = QueryDict(settings.filter_querystring).dict()
            orders = params.pop('o', '').split('.')
            fields = params.pop('fields', '').split(',')

            for ignore in IGNORED_PARAMS:
                params.pop(ignore, None)

            if not dataset:
                return params

            dataset = dataset.filter(**params)

            if '' not in orders and '' not in fields:
                ordering = []
                for order in orders:
                    field = fields[abs(int(order))]
                    if int(order) < 0:
                        field = '-{}'.format(field)
                    ordering.append(field)
                dataset = dataset.order_by(*ordering)

        return dataset

    def prepare_export_dataset(self, settings):
        current_model = make_model_class(settings)

        if settings.dataset:
            dataset = self.get_or_raise('dataset', settings.dataset)
            dataset = dataset(current_model, settings)
        else:
            dataset = current_model._default_manager.all()

        dataset = self.filter_dataset(settings, dataset)

        return dataset

    def prepare_export_data(self, processor, queryset):
        """Prepare data using filters from settings
        and return data with dimensions"""

        settings = processor.settings
        model = make_model_class(settings)
        msettings = model_settings(model)

        exclude = msettings.get('exclude', [])

        fields = settings.fields_with_converters()
        fields = list(filterfalse(
            lambda f: f.attribute in exclude, fields))

        if settings.end_row:
            rows = settings.end_row
            if settings.start_row:
                rows -= settings.start_row
                rows += 1

            queryset = queryset[:rows]

        mfields = model_fields(model)

        return {
            'rows': queryset.count(),
            'cols': len(fields),
            'fields': fields,
            'mfields': mfields,
            'items': (
                self.convert_value(
                    process_attribute(item, field.attribute),
                    field, export=True)
                for item in queryset
                for field in fields
            )
        }

    def prepare_handlers(self, key_name, processor, model, context=None):
        prepares = []
        handlers = getattr(self, self._make_key(key_name))
        for handler in handlers.keys():
            if processor.settings.data_action in handler:
                prepares.append(handlers[handler])

        context = context or {}
        for prepare in prepares:
            context = prepare(model, context)

        return context

    def prepare_context(self, settings, path):
        context = {}
        contexts = settings.contexts.all()

        if not contexts:
            return {}

        processor = self.make_processor(settings)
        max_rows, max_cols = processor.open(path)
        processor.set_dimensions(
            0, 0, max_rows, max_cols,
            import_data=True)
        processor._read_from_start = True

        for field in contexts:
            context[field.name] = field.value or cell_value(
                None, field.cell, processor)

        return context

    def prepare_import_data(self, processor, model):
        """Prepare data using filters from settings and return iterator"""

        settings = processor.settings
        fields = list(settings.fields_with_converters())
        mfields = model_fields(model) if model else {}

        # TODO: refactor

        return {
            'cols': len(fields),
            'fields': fields,
            'items': self.model_data(settings, processor, model, fields),
            'mfields': mfields
        }

    def import_data(self, settings, path=None):
        """Import data to database"""

        if settings.language:
            activate(settings.language)

        processor = self.make_processor(settings)
        model = make_model_class(settings)

        return processor.import_data(model, path)

    def prepare_import_dataset(self, settings, processor, model, fields):
        """Get data from diferent source registered at dataset"""

        if settings.dataset:
            dataset = self.get_or_raise('dataset', settings.dataset)
            dataset = dataset(model, settings)

            for index, row in enumerate(dataset):
                yield index, row
        else:
            for index in processor.rows:
                yield index, processor.read(index)

    def model_data(self, settings, processor, model, fields):
        dataset = self.prepare_import_dataset(
            settings, processor, model, fields)

        for index, row in dataset:
            _model = {}

            for index, field in enumerate(fields):
                value = cell_value(row, field.name or index)
                _model[field.attribute] = self.convert_value(value, field)

            yield index, _model


class Manager(object):

    """Manager for data processors"""

    def __init__(self):
        self.processors = OrderedDict()
        self.actions = OrderedDict()
        self.converters = OrderedDict()
        self.datasets = OrderedDict()
        self.befores = OrderedDict()
        self.afters = OrderedDict()
        self.errors = OrderedDict()

        self.imported = False

    def _make_key(self, key):
        return '{}s'.format(key)

    def get_or_raise(self, name, key):
        # TODO: remove method

        value = getattr(self, self._make_key(name), {})
        value = value.get(key, None)

        if value is None:
            raise ItemDoesNotRegistered(
                '{} not registered at {}'.format(key, name))

        return value

    def has(self, name, key):
        for value in getattr(self, self._make_key(name), {}).values():
            if value == key:
                return True
        return False

    def _register_dict(self, type_name, func_name, label, **kwargs):
        """Return decorator for adding functions as key, value
        to instance, dict"""

        def decorator(func):
            key = self._make_key(type_name)
            values = getattr(self, key, OrderedDict())
            position = getattr(func, 'position', 0)
            new_name = func_name or func.__name__

            func.label = label
            func.use_transaction = kwargs.get('use_transaction', False)

            if values is not None:
                if values.get(new_name, None) is not None:
                    raise ItemAlreadyRegistered(
                        '{} already registred at {}'.format(new_name, key))

                values[new_name] = func
                if position:
                    values = OrderedDict(
                        sorted(
                            values.items(),
                            key=lambda p: getattr(p[1], 'position', 0)))
                setattr(self, key, values)

            return func

        return decorator

    def register(self, type_name, label=None, name=None, item=None, **kwargs):
        """Decorator and function to config new processors, handlers"""

        func = self._register_dict(type_name, name, label, **kwargs)

        return func(item) if item else func

    def unregister(self, type_name, item=None):
        """Decorator to pop dict items"""

        items = getattr(self, self._make_key(type_name), None)
        if items is not None:
            items.pop(getattr(item, '__name__', item), None)

        return item

    def import_dependecies(self):
        """Import modules within aditional paths"""

        if not self.imported:
            modules = SETTINGS['PROCESSORS'] + SETTINGS['ACTIONS'] \
                + SETTINGS['CONVERTERS']

            for module in modules:
                __import__(module)

            self.imported = True

manager = Manager()
manager.import_dependecies()
