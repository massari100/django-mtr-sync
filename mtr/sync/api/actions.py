from django.db import models

from .manager import manager
from ..helpers import gettext_lazy as _


def _find_instance(filters, model, key=None, marker=None):
    instance = None
    filter_attrs = {}

    for k, v in filters.items():
        if key and '{}{}'.format(key, marker or '') in k:
            if marker:
                k = k.split(marker)[1]
            filter_attrs[k] = v
        elif '|_fk_|' not in k and '|_m_|' not in k and not key:
            filter_attrs[k] = v

    if filter_attrs.keys():
        instance = model._default_manager \
            .filter(**filter_attrs).first()

    return instance


def _create_related_instance(instance, filters, related_model, key, attrs):
    related_instance = _find_instance(filters, related_model, key, '|_fk_|')

    if related_instance is None:
        related_instance = related_model(**attrs[key])
        related_instance.save()

        setattr(instance, key, related_instance)


def _create_mtm_instance(
        add_after, instance, filters, related_model, key, related_models):
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
        related_instance = _find_instance(filters, related_model, key, '|_m_|')

        if related_instance is None:
            item = related_model(**instance_attr)
            item.save()

            add_after.setdefault(key, []).append(item)

    return add_after


def filter_fields(filter_params, model_attrs, fields, remove_markers=True):
    for field in filter(lambda f: f.find, fields):
        field_name = field.attribute
        if remove_markers:
            field_name = field_name.replace('|_fk_|', '__') \
                .replace('|_m_|', '__')
        field_value = model_attrs[field.attribute] or field.update_value
        field_filter = field_name

        if field.find_filter:
            field_filter = '{}__{}'.format(field_name, field.find_filter)
        filter_params.update(**{field_filter: field_value})

    return filter_params


def filter_attrs(model_attrs, fields, mfields):
    update_fields = list(filter(lambda f: f.update, fields)) or fields
    update_values = {}

    for field in update_fields:
        if '_|' not in field.attribute and \
                isinstance(mfields[field.attribute], models.Field):
            update_values[field.attribute] = model_attrs[field.attribute] \
                or field.update_value

    return update_values


def find_instances(model, model_attrs, params, fields):
    filter_params = params
    instances = model._default_manager.all()

    filter_params = filter_fields(filter_params, model_attrs, fields)

    if filter_params.keys():
        instances = instances.filter(**filter_params)

    return instances


@manager.register('action', _('Create only'))
def create(model, model_attrs, related_attrs, context, **kwargs):
    filters = filter_fields(
        {}, kwargs['raw_attrs'], kwargs['fields'], remove_markers=False)
    model_attrs = filter_attrs(
        model_attrs, kwargs['fields'], kwargs['mfields'])
    fields = kwargs['mfields']

    instance = _find_instance(filters, model)
    if instance is None:
        instance = model(**model_attrs)

    add_after = {}

    for key in related_attrs.keys():
        related_field = fields.get(key)
        related_model = related_field.rel.to

        if isinstance(related_field, models.ForeignKey):
            _create_related_instance(
                instance, filters, related_model, key, related_attrs)

        elif isinstance(related_field, models.ManyToManyField):
            _create_mtm_instance(
                add_after, instance, filters,
                related_model, key, related_attrs)

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


@manager.register('action', _('Update or create'))
def update_or_create(model, model_attrs, related_attrs, context, **kwargs):
    instances = update(model, model_attrs, related_attrs, context, **kwargs)

    if not instances:
        create(model, model_attrs, related_attrs, context, **kwargs)
