from __future__ import unicode_literals

from django.utils.six.moves import filterfalse
from django.utils.translation import activate
from django.http import QueryDict
from django.contrib.admin.views.main import IGNORED_PARAMS

from mtr.utils.manager import BaseManager

from .helpers import make_model_class, process_attribute, \
    model_fields, cell_value, model_settings
from ..settings import SETTINGS


class Manager(BaseManager):

    """Manager for data processors"""

    def convert_value(self, value, field, export=False, action=None):
        """Process value with filters and actions"""

        convert_action = 'export' if export else 'import'

        for convert_func in field.ordered_converters:
            value = convert_func(value, convert_action)

        return value

    def processor_choices(self):
        """Return all registered processors"""

        for name, processor in self.all('processor').items():
            yield (
                name,
                '{} | {}'.format(
                    processor.file_format,
                    processor.file_description))

    def dataset_choices(self):
        """Return all registered data sources"""

        for name, dataset in self.all('dataset').items():
            yield(name, getattr(dataset, 'label', dataset.__name__))

    def action_choices(self):
        """Return all registered actions"""

        for name, action in self.all('action').items():
            yield(name, getattr(action, 'label', action.__name__))

    def converter_choices(self):
        """Returns all registered converters"""

        for name, converter in self.all('converter').items():
            yield(name, getattr(converter, 'label', converter.__name__))

    def make_processor(self, settings, from_extension=False):
        """Create new processor instance if exists"""

        processor = None

        if from_extension:
            extension = settings.buffer_file.path.split('.')[-1]
            for pr in self.all('processors').values():
                if pr.file_format.strip('.') == extension:
                    processor = pr
                    settings.processor = processor.__name__
                    break

        processor = self.get('processor', settings.processor)

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
            dataset = self.get('dataset', settings.dataset)
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

        msettings = model_settings(model, 'sync')
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
        handlers = self.all(key_name) or {}
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
            dataset = self.get('dataset', settings.dataset)
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


manager = Manager()
manager.import_modules(
    SETTINGS['DEFAULT'] + SETTINGS['PROCESSORS'] +
    SETTINGS['ACTIONS'] + SETTINGS['CONVERTERS'])
