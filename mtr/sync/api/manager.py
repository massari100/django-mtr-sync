from __future__ import unicode_literals

from collections import OrderedDict

from django.utils.six.moves import filterfalse
from django.utils.translation import activate
from django.http import QueryDict
from django.contrib.admin.views.main import IGNORED_PARAMS

from .exceptions import ItemAlreadyRegistered, ItemDoesNotRegistered
from .helpers import make_model_class, model_settings, \
    process_attribute, model_fields, cell_value
from ..settings import SETTINGS


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
            'items': self.model_data(processor, model, fields),
            'mfields': mfields
        }

    def import_data(self, settings, path=None):
        """Import data to database"""

        if settings.language:
            activate(settings.language)

        processor = self.make_processor(settings)
        model = make_model_class(settings)

        return processor.import_data(model, path)

    def model_data(self, processor, model, fields):
        for row_index in processor.rows:
            _model = {}
            row = processor.read(row_index)

            for index, field in enumerate(fields):
                value = cell_value(row, field.name or index)
                _model[field.attribute] = self.convert_value(value, field)

            yield row_index, _model


class Manager(ProcessorManagerMixin):

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
        """Return decorator for adding functions as key, value to dict
        and send manager_registered signal to handle new params"""

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
