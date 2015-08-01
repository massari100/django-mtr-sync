from django.conf import settings

if 'celery' in settings.INSTALLED_APPS:
    from celery import shared_task as job
elif 'django_rq' in settings.INSTALLED_APPS:
    from django_rq import job

from .lib.manager import manager
from .models import Settings
from .helpers import make_from_params


@job
def export_data(params, data=None):
    manager.export_data(
        make_from_params(Settings, params), data)


@job
def import_data(params, path=None):
    manager.import_data(
        make_from_params(Settings, params), path)
