from celery import shared_task

from .api import manager
from .models import Settings


@shared_task
def export_data(params):
    settings_id = params.get('id', False)
    if settings_id:
        settings = Settings.object.get(pk=settings_id)
    else:
        settings = Settings(**params)

    manager.export_data(settings)


@shared_task
def import_data():
    return True


@shared_task
def check_periodic_export():
    pass
