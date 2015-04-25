import traceback

from django.utils.translation import gettext_lazy as _
from django.db import transaction, Error, models

from .manager import manager
from .exceptions import ErrorChoicesMixin
from .signals import error_raised
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


def _create_instances(model, model_attrs, related_models):
    instance = model(**model_attrs)
    fields = model_fields(model)
    add_after = {}

    for key in related_models.keys():
        related_field = fields.get(key)
        related_model = related_field.rel.to

        if isinstance(related_field, models.ForeignKey):
            _create_related_instance(
                instance, related_model, key, related_models)

        elif isinstance(related_field, models.ManyToManyField):
            _create_mtm_instance(
                add_after, instance, related_model, key, related_models)

    instance.save()

    for key, values in add_after.items():
        getattr(instance, key).add(*values)


@manager.register('action',
    label=_('mtr.sync:Create instances without filter'))
def create(row, model, model_attrs, related_attrs, processor):
    sid = transaction.savepoint()

    try:
        with transaction.atomic():
            _create_instances(model, model_attrs, related_attrs)
    except (Error, ValueError,
            AttributeError, TypeError, IndexError):

        transaction.savepoint_rollback(sid)
        error_message = traceback.format_exc()
        if 'File' in error_message:
            error_message = 'File{}'.format(
                error_message.split('File')[-1])

        value = {
            'model_attrs': model_attrs,
            'related_attrs': related_attrs
        }

        error_raised.send(processor,
            error=error_message,
            position=row,
            value=value,
            step=ErrorChoicesMixin.IMPORT_DATA)
