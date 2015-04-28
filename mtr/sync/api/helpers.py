from collections import OrderedDict

from django.utils.six.moves import filterfalse
from django.db import models
from django.db.models.fields import Field as ModelField

from ..settings import MODEL_SETTINGS_NAME

_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


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

    for index in range(0, 18279):
        name = column_name(index)
        if name == value:
            return index

    raise IndexError


def column_value(value):
    """Return column index or convert from value"""

    if isinstance(value, int):
        return value

    if value.isdigit():
        return int(value)

    return column_index(value)


def model_settings(model):
    return getattr(model, MODEL_SETTINGS_NAME(), {})


def models_list():
    # TODO: get models deprecation

    mlist = filterfalse(
        lambda m: model_settings(m).get('ignore', False),
        models.get_models())

    return mlist


def model_fields(model):
    """Return model field or custom method"""

    opts = model._meta
    sortable_virtual_fields = [
        f for f in opts.virtual_fields
        if isinstance(f, ModelField)]
    fields_arr = sorted(
        list(opts.concrete_fields) +
        list(sortable_virtual_fields) + list(opts.many_to_many))

    msettings = model_settings(model)
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


def model_attributes(settings, prefix=None, model=None, parent=None):
    """Return iterator of fields names by given mode_path"""

    model = model or make_model_class(settings)

    for name, field in model_fields(model).items():
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
            field, 'short_description', getattr(
                field, 'verbose_name', getattr(
                    field, '__name__', repr(field))))

        if m_prefix:
            child_attrs = model_attributes(
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


def make_model_class(settings):
    """Return class for name in model"""

    for mmodel in models_list():
        if settings.model == '{}.{}'.format(
                mmodel._meta.app_label, mmodel.__name__).lower():
            return mmodel


def model_choices():
    """Return all registered django models as choices"""

    yield ('', '-' * 9)

    for model in models_list():
        yield (
            '{}.{}'.format(
                model._meta.app_label.lower(),
                model.__name__.lower()),
            '{} | {}'.format(
                model._meta.app_label.title(),
                model._meta.verbose_name.title()))


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
