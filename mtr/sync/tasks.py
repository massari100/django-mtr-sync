from django.conf import settings

from .lib.manager import manager
from .models import Settings
from ..utils.helpers import make_from_params
from .settings import SETTINGS

if 'django_rq' in settings.INSTALLED_APPS and SETTINGS['BROKER'] == 'rq':
    from django_rq import job as rq_job

    def job(f): return rq_job(f, timeout=86400)
elif 'celery' in settings.INSTALLED_APPS and SETTINGS['BROKER'] == 'celery':
    from celery import shared_task as job
else:
    def func(f): return f
    job = func


@job
def export_data(params, data=None):
    manager.export_data(make_from_params(Settings, params), data)


@job
def import_data(params, path=None):
    manager.import_data(make_from_params(Settings, params), path)
