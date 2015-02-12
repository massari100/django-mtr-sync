from celery import shared_task

from .api import manager
from .models import Settings


@shared_task
def export_data(params, data=None):
    settings = Settings.make_from_params(params)

    manager.export_data(settings, data)


@shared_task
def import_data():
    return True


@shared_task
def check_periodic_export():
    pass
