from celery import shared_task

from .api import manager
from .models import Settings
from .helpers import make_from_params


@shared_task
def export_data(params, data=None):
    manager.export_data(
        make_from_params(Settings, params), data)


@shared_task
def import_data(params, path=None):
    manager.import_data(
        make_from_params(Settings, params), path)
