from __future__ import unicode_literals

from collections import OrderedDict

from django.utils.six.moves import filterfalse
from django.db import models
from django.db.models.fields import Field as ModelField

from .exceptions import ItemAlreadyRegistered, ItemDoesNotRegistered
from .signals import manager_registered
from ..settings import IMPORT_PROCESSORS, MODEL_SETTINGS_NAME


class ModelManagerMixin(object):
    # TODO: refactor model fields managament

    def get_model_fields(self, model):
        """Return model field or custom method"""

        opts = model._meta
        sortable_virtual_fields = [f for f in opts.virtual_fields
            if isinstance(f, ModelField)]
        fields_arr = sorted(
            opts.concrete_fields + sortable_virtual_fields + opts.many_to_many)

        msettings = self.model_settings(model)
        exclude = msettings.get('exclude', [])
        custom_fields = msettings.get('custom_fields', [])
        ordered_fields = []

        for field in fields_arr:
            if field.name not in exclude:
                ordered_fields.append((field.name, field))

        for field in custom_fields:
            if field not in exclude:
                ordered_fields.append((field, getattr(model, field, None)))

        return OrderedDict(ordered_fields)

    def model_settings(self, model):
        return getattr(model, MODEL_SETTINGS_NAME(), {})

    def models_list(self):
        mlist = filterfalse(
            lambda m: self.model_settings(m).get('ignore', False),
            models.get_models())

        return mlist

    def model_attributes(self, settings, prefix=None, model=None, parent=None):
        """Return iterator of fields names by given mode_path"""

        model = model or self.model_class(settings)

        for name, field in self.get_model_fields(model).items():
            label = name
            child_attrs = None
            m_prefix = None

            if isinstance(field, models.ForeignKey):
                m_prefix = '{}|_fk_|'
            elif isinstance(field, models.ManyToManyField):
                m_prefix = '{}|_m_|'
            elif isinstance(field, property):
                field = field.fget

            label = getattr(
                field, '__name__', getattr(
                    field, 'short_description', getattr(
                        field, 'verbose_name', repr(field))))

            if m_prefix:
                child_attrs = self.model_attributes(
                        settings, m_prefix.format(name),
                        model=field.rel.to, parent=model)
            if prefix:
                name = ''.join((prefix, name))

            if child_attrs:
                for name, label in child_attrs:
                    yield (name, '{} | {}'.format(
                        field.rel.to._meta.verbose_name, label).capitalize())
            else:
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

    def process_attribute(self, model, attribute):
        """Process all atribute path to retrieve value"""

        # TODO: refactor attributes

        if '|_fk_|' in attribute:
            attributes = attribute.split('|_fk_|')
            attr = getattr(model, attributes[0], None)

            if '|_' in attributes[1]:
                attr = self.process_attribute(self, attr, attributes[1])
            else:
                attr = getattr(attr, attributes[1], None)
        elif '|_m_|' in attribute:
            attributes = attribute.split('|_m_|')
            attr = getattr(model, attributes[0], None)

            if '|_' in attributes[1]:
                attr = self.process_attribute(self, attr, attributes[1])
            else:
                if attr:
                    attr = attr.all()
                    value = []

                    for item in attr:
                        value.append(getattr(item, attributes[1], None))

                    return value
                else:
                    return []

                attr = getattr(attr, attributes[1], None)
        else:
            attr = getattr(model, attribute, None)

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
        """Process value with filters and actions"""

        process_action = 'export' if export else 'import'
        for field_filter in field.filters_queue:
            action, value = self.process_filter(
                field, field_filter, value, process_action)

        if export:
            return value
        else:
            return action, value

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
        model = self.model_class(settings)
        msettings = self.model_settings(model)

        exclude = msettings.get('exclude', [])

        fields = settings.fields_with_filters()
        fields = list(filterfalse(
            lambda f: f.attribute in exclude, fields))

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
                    field, self.process_attribute(
                        item, field.attribute), export=True)
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
        # TODO: split functionality for mixins init here

        pass

    def _make_key(self, key):
        return '{}s'.format(key)

    def get_or_raise(self, name, key):
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

    def _register_dict(self, type_name, func_name, **kwargs):
        """Return decorator for adding functions as key, value to dict
        and send manager_registered signal to handle new params"""

        def decorator(func):
            key = self._make_key(type_name)
            values = getattr(self, key, OrderedDict())
            position = getattr(func, 'position', 0)
            new_name = func_name or func.__name__

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

                kwargs.update({
                    'type_name': type_name,
                    'func_name': new_name,
                    'func': func
                })
                manager_registered.send(self, **kwargs)

            return func

        return decorator

    def register(self, type_name, item=None, name=None, **kwargs):
        """Decorator and function to config new processors, handlers"""

        func = self._register_dict(type_name, name, **kwargs)

        return func(item) if item else func

    def unregister(self, type_name, item=None):
        """Decorator to pop dict items"""

        items = getattr(self, self._make_key(type_name), None)
        if items is not None:
            items.pop(getattr(item, '__name__', item), None)

        return item

    def import_processors_modules(self):
        """Import modules within IMPORT_PROCESSORS paths"""

        for module in IMPORT_PROCESSORS():
            __import__(module)

manager = Manager()
manager.import_processors_modules()
