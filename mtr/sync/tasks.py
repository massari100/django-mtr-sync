from celery import shared_task

from .api import manager


@shared_task
def export_data(params, data=None):
    manager.export_data(params, data, from_params=True)


@shared_task
def import_data():
    return True


@shared_task
def check_periodic_export():
    pass
