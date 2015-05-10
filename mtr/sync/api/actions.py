from django.utils.translation import gettext_lazy as _
from django.db import models

from .manager import manager
from .helpers import model_fields


def _create_related_instance(instance, related_model, key, related_models):
    related_instance = related_model(**related_models[key])
    related_instance.save()

    setattr(instance, key, related_instance)


def _create_mtm_instance(
        add_after, instance, related_model, key, related_models):
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
        item = related_model(**instance_attr)
        item.save()
        add_after.setdefault(key, []).append(item)

    return add_after


@manager.register(
    'action',
    label=_('mtr.sync:Create only'))
def create(model, model_attrs, related_attrs, **kwargs):
    instance = model(**model_attrs)
    fields = model_fields(model)
    add_after = {}

    for key in related_attrs.keys():
        related_field = fields.get(key)
        related_model = related_field.rel.to

        if isinstance(related_field, models.ForeignKey):
            _create_related_instance(
                instance, related_model, key, related_attrs)

        elif isinstance(related_field, models.ManyToManyField):
            _create_mtm_instance(
                add_after, instance, related_model, key, related_attrs)

    instance.save()

    for key, values in add_after.items():
        getattr(instance, key).add(*values)


@manager.register(
    'action', label=_('mtr.sync:Update only'))
def update(model, model_attrs, related_attrs, **kwargs):
    filter_params = kwargs['params']
    updating_fields = kwargs['fields']
    updating_fields = list(filter(lambda f: f.update, kwargs['fields'])) \
        or kwargs['fields']

    for field in filter(lambda f: f.find, kwargs['fields']):
        field_name = field.attribute .replace('|_fk_|', '__') \
            .replace('|_m_|', '__')
        field_value = model_attrs[field.attribute] or field.update_value
        field_filter = field_name
        if field.find_filter:
            field_filter = '{}__{}'.format(field_name, field.find_filter)
        filter_params.update(**{field_filter: field_value})

    if filter_params.keys():
        instances = model._default_manager.filter(**filter_params)

    update_values = {}
    for field in updating_fields:
        if '_|' not in field.attribute:
            update_values[field.attribute] = model_attrs[field.attribute] \
                or field.update_value

    instances.update(**update_values)
