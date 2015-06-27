from django.db import models

from .manager import manager
from ..helpers import gettext_lazy as _


def _find_instance(filters, model):
    instance = None
    filters, can_create = filters

    if filters and can_create:
        instance = model._default_manager \
            .filter(**filters).first()

    return instance, can_create


def _create_related_instance(instance, filters, related_model, attrs, key):
    related_instance, can_create = _find_instance(filters, related_model)

    if not can_create:
        return

    if related_instance is None:
        related_instance = related_model(**attrs[key])
        related_instance.save()

    setattr(instance, key, related_instance)


def _create_mtm_instance(
        add_after, instance, filters, related_model, related_models, key):
    instance_attrs = []
    rel_values = list(related_models[key].values())
    indexes = len(rel_values[0])

    for index in range(indexes):
        instance_values = {}
        for k in related_models[key].keys():
            value = related_models[key][k][index]
            instance_values[k] = value
        instance_attrs.append(instance_values)

    for instance_attr in instance_attrs:
        related_instance, can_create = _find_instance(filters, related_model)

        if not can_create:
            continue

        if related_instance is None:
            item = related_model(**instance_attr)
            item.save()
        else:
            item = related_instance

        add_after.setdefault(key, []).append(item)

    return add_after


def filter_fields(
        model_attrs, fields, key=None, can_create=True, params=None):
    filter_params = params or {}

    for field in filter(lambda f: f.find, fields):
        field_value = field.find_value or model_attrs[field.attribute]

        if field.find_filter:
            filter_attr = field.attribute

            if key and key in field.attribute:
                filter_attr = filter_attr.split(key)[1]
            elif '|_' in field.attribute or key is not None:
                continue

            field_filter = '{}__{}'.format(filter_attr, field.find_filter)
            filter_params[field_filter] = field_value

        if can_create and field.set_filter == 'not' and not field_value:
            can_create = False

    return filter_params, can_create


def filter_attrs(model_attrs, fields, mfields):
    update_fields = list(filter(lambda f: f.update, fields)) or fields
    update_values = {}

    for field in update_fields:
        if '_|' not in field.attribute and \
                isinstance(mfields[field.attribute], models.Field):
            update_values[field.attribute] = field.set_value or \
                model_attrs[field.attribute]

    return update_values


def find_instances(model, model_attrs, params, fields):
    filter_params = params
    instances = model._default_manager.all()

    filter_params, can_create = filter_fields(
        model_attrs, fields, can_create=False, params=filter_params)

    if filter_params.keys():
        instances = instances.filter(**filter_params)

    return instances


@manager.register('action', _('Create only'))
def create(model, model_attrs, related_attrs, context, **kwargs):
    instance_filters = filter_fields(kwargs['raw_attrs'], kwargs['fields'],)
    fk_filters = filter_fields(kwargs['raw_attrs'], kwargs['fields'], '|_fk_|')
    mtm_filters = filter_fields(kwargs['raw_attrs'], kwargs['fields'], '|_m_|')

    model_attrs = filter_attrs(
        model_attrs, kwargs['fields'], kwargs['mfields'])
    fields = kwargs['mfields']

    instance, can_create = _find_instance(
        instance_filters, model)

    if not can_create:
        return instance

    if instance is None:
        instance = model(**model_attrs)

    add_after = {}

    for key in related_attrs.keys():
        related_field = fields.get(key)
        related_model = related_field.rel.to

        if isinstance(related_field, models.ForeignKey):
            _create_related_instance(
                instance, fk_filters, related_model,
                related_attrs, key)

        elif isinstance(related_field, models.ManyToManyField):
            _create_mtm_instance(
                add_after, instance, mtm_filters,
                related_model, related_attrs, key)

    instance.save()

    for key, values in add_after.items():
        getattr(instance, key).add(*values)

    return instance


@manager.register('action', _('Update only'))
def update(model, model_attrs, related_attrs, context, **kwargs):
    update_values = filter_attrs(
        model_attrs, kwargs['fields'], kwargs['mfields'])

    instances = find_instances(
        model, kwargs['raw_attrs'], kwargs['params'], kwargs['fields'])

    instances.update(**update_values)

    return instances
