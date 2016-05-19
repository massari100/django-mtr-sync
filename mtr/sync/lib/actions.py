from django.db import models

from .manager import manager
from ..translation import gettext_lazy as _

from mtr.utils.helpers import update_instance


def find_instance(filters, model):
    instance = None
    filters, can_create = filters

    if filters and can_create:
        instance = model._default_manager \
            .filter(**filters).first()

    return instance, can_create


def create_related_instance(
        instance, filters, related_model, attrs, key, updated_attrs):
    related_instance, can_create = find_instance(filters, related_model)

    if not can_create:
        return

    if related_instance is None:
        related_instance = related_model(**attrs[key])
        related_instance.save()

        setattr(instance, key, related_instance)
    elif updated_attrs:
        related_instance = update_instance(related_instance, updated_attrs)


def create_mtm_instance(
        add_after,
        instance, filters, related_model,
        related_models, key, updated_attrs):
    instances_attrs = []
    rel_values = list(related_models[key].values())
    indexes = len(rel_values[0])

    for index in range(indexes):
        instance_values = {}
        for k in related_models[key].keys():
            value = related_models[key][k][index]
            instance_values[k] = value
        instances_attrs.append(instance_values)

    for instance_attrs in instances_attrs:
        related_instance, can_create = find_instance(filters, related_model)

        if not can_create:
            continue

        if related_instance is None:
            related_instance = related_model(**instance_attrs)
            related_instance.save()

            add_after.setdefault(key, []).append(related_instance)
        elif updated_attrs:
            related_instance = update_instance(related_instance, updated_attrs)

    return add_after


def filter_fields(
        model_attrs, fields, key=None, can_create=True, params=None):
    filter_params = params or {}

    for field in (field for field in fields if field.find):
        field_value = field.find_value or model_attrs[field.attribute]

        if field.find_filter:
            filter_attr = field.attribute
            find_filter = field.find_filter

            if key and key in field.attribute:
                filter_attr = filter_attr.split(key)[1]
                find_filter = find_filter if find_filter != 'exact' else 'in'
            elif '|_' in field.attribute or key is not None:
                continue

            field_filter = '{}__{}'.format(filter_attr, find_filter)
            filter_params[field_filter] = field_value

        if can_create and field.set_filter == 'not' and not field_value:
            can_create = False

    return filter_params, can_create


def filter_attrs(raw_attrs, fields, mfields, name=None):
    update_fields = list(filter(lambda f: f.update, fields)) or fields
    update_values = {}

    for field in update_fields:
        if ('_|' not in field.attribute and name is None) or \
                (name and name in field.attribute):
            update_values[field.attribute] = field.set_value or \
                raw_attrs[field.attribute]

    return update_values


def find_instances(model, model_attrs, params, fields):
    filter_params = params
    instances = model._default_manager.all()

    filter_params, can_create = filter_fields(
        model_attrs, fields, can_create=False, params=filter_params)

    if filter_params.keys():
        instances = instances.filter(**filter_params)

    return instances


@manager.register('action', _('Create only'), use_transaction=True)
def create(model, model_attrs, related_attrs, context, **kwargs):
    update = kwargs.get('update', False)
    save_instance = False
    add_after = {}
    fk_updated_attrs, m_updated_attrs = None, None

    instance_filters = filter_fields(kwargs['raw_attrs'], kwargs['fields'])
    fk_filters = filter_fields(kwargs['raw_attrs'], kwargs['fields'], '|_fk_|')
    m_filters = filter_fields(kwargs['raw_attrs'], kwargs['fields'], '|_m_|')

    if update:
        fk_updated_attrs = filter_attrs(
            kwargs['raw_attrs'], kwargs['fields'], kwargs['mfields'], '|_fk_|')
        m_updated_attrs = filter_attrs(
            kwargs['raw_attrs'], kwargs['fields'], kwargs['mfields'], '|_m_|')

    instance, can_create = find_instance(instance_filters, model)

    if not can_create:
        return context

    if instance is None:
        instance = model(**model_attrs)
        save_instance = True
    elif update:
        updated_attrs = filter_attrs(
            kwargs['raw_attrs'], kwargs['fields'], kwargs['mfields'])
        instance = update_instance(instance, updated_attrs)

    for key in related_attrs.keys():
        related_field = kwargs['mfields'].get(key)
        related_model = related_field.rel.to

        if isinstance(related_field, models.ForeignKey):
            create_related_instance(
                instance, fk_filters, related_model,
                related_attrs, key, fk_updated_attrs)

        elif isinstance(related_field, models.ManyToManyField):
            create_mtm_instance(
                add_after,
                instance, m_filters, related_model,
                related_attrs, key, m_updated_attrs)

    if save_instance:
        instance.save()

    for key, instances in add_after.items():
        getattr(instance, key).add(*instances)

    return context


@manager.register('action', _('Create or update'), use_transaction=True)
def create_or_update(*args, **kwargs):
    kwargs['update'] = True
    return create(*args, **kwargs)


@manager.register('action', _('Update only'), use_transaction=True)
def update(model, model_attrs, related_attrs, context, **kwargs):
    updated_values = filter_attrs(
        kwargs['raw_attrs'], kwargs['fields'], kwargs['mfields'])

    instances = find_instances(
        model, kwargs['raw_attrs'], kwargs['params'], kwargs['fields'])

    for instance in instances:
        update_instance(instance, updated_values)

    return context
