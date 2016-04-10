from collections import OrderedDict

from django.utils.encoding import smart_text
from django.db import models
from django.conf import settings as django_settings
from django.db.models.fields import Field as ModelField

from mtr.utils.helpers import model_settings, models_list, model_app_name

_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_symbols = (':', '|', ',', '+', '-')


def cell_value(row, cols, processor=None):
    # TODO: refactor to normal cell parsing with cells indexes

    if isinstance(cols, int):
        return row[cols]

    # TODO: use regex
    no_symbols_finded = True
    for symbol in _symbols:
        if symbol in cols:
            no_symbols_finded = False
            break

    if no_symbols_finded:
        return row[column_index(cols)]

    items = []

    for item in cols.split('+'):
        value = []
        joiner = None

        if '|' in item:
            item, joiner = item.split('|')

        for col in item.split(','):
            if processor and ':' in col:
                col, row = col.split(':')
                row = processor.read(int(row)-1)
            if '-' in col:
                start, end = col.split('-')
                value += row[column_index(start):column_index(end)+1]
            else:
                value.append(row[column_index(col)])
        if joiner is not None:
            joiner = joiner or ' '
            value = joiner.join(map(lambda v: smart_text(v), value))

        if '+' in cols:
            items.append(value)
        else:
            items = value

    return items


def column_name(index):
    """Return column name for given index"""
    name = ''

    while True:
        q, r = divmod(index, 26)
        name = _chars[r] + name

        if not q:
            return name

        index = q - 1


def column_index(value):
    """Return column index for given name"""

    if isinstance(value, int):
        return value

    if value.isdigit():
        return int(value)

    for index in range(0, 18279):
        name = column_name(index)
        if name == value:
            return index

    raise IndexError


def model_fields(model, settings=None):
    """Return model field or custom method"""

    opts = model._meta
    sortable_virtual_fields = [
        f for f in opts.virtual_fields
        if isinstance(f, ModelField)]
    fields_arr = sorted(
        list(opts.concrete_fields) +
        list(sortable_virtual_fields) + list(opts.many_to_many))

    msettings = model_settings(model, 'sync')
    exclude = msettings.get('exclude', [])
    custom_fields = msettings.get('custom_fields', [])
    ordered_fields = []
    hide_translation_fields = getattr(
        settings, 'hide_translation_fields', False)

    for field in fields_arr:
        if field.name not in exclude:
            add_it = True
            if hide_translation_fields:
                for lang, name in django_settings.LANGUAGES:
                    if field.name.endswith('_{}'.format(lang)):
                        add_it = False
            if add_it:
                ordered_fields.append((field.name, field))

    for field in custom_fields:
        if field not in exclude:
            ordered_fields.append((field, getattr(model, field, None)))

    return OrderedDict(ordered_fields)


def model_attributes(settings, prefix=None, model=None, parent=None, level=0):
    """Return iterator of fields names by given model in settings"""

    model = model or make_model_class(settings)
    include_related = True and settings.include_related

    for name, field in model_fields(model, settings).items():
        label = name
        child_attrs = None
        m_prefix = None

        if level > 1:
            continue

        if isinstance(field, models.ForeignKey):
            if not include_related:
                continue
            m_prefix = '{}|_fk_|'
        elif isinstance(field, models.ManyToManyField):
            if not include_related:
                continue
            m_prefix = '{}|_m_|'
        elif isinstance(field, property):
            field = field.fget

        label = getattr(
            field, 'short_description', getattr(
                field, 'verbose_name', getattr(
                    field, '__name__', repr(field))))

        if m_prefix:
            child_attrs = []
            child_attrs = model_attributes(
                    settings, m_prefix.format(name),
                    model=field.rel.to, parent=model, level=level+1)
        if prefix:
            name = ''.join((prefix, name))

        if child_attrs:
            for name, label in child_attrs:
                yield (name, smart_text('{} | {}').format(
                    field.rel.to._meta.verbose_name, label).capitalize())
        else:
            yield (name, label.capitalize())


def make_model_class(settings):
    """Return class for name in model"""

    for model in models_list():
        if settings.model == model_app_name(model):
            return model


def _process_fk_attribute(model, attribute):
    attributes = attribute.split('|_fk_|')
    attr = getattr(model, attributes[0], None)

    if '|_' in attributes[1]:
        attr = process_attribute(attr, attributes[1])
    else:
        attr = getattr(attr, attributes[1], None)

    return attr


def _process_mtm_attribute(model, attribute):
    attributes = attribute.split('|_m_|')
    attr = getattr(model, attributes[0], None)

    if '|_' in attributes[1]:
        attr = process_attribute(attr, attributes[1])
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

    return attr


def process_attribute(model, attribute):
    """Process all atribute path to retrieve value"""

    if '|_fk_|' in attribute:
        attr = _process_fk_attribute(model, attribute)
    elif '|_m_|' in attribute:
        attr = _process_mtm_attribute(model, attribute)
    else:
        attr = getattr(model, attribute, None)

    return attr
