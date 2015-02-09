from celery import shared_task


@shared_task
def export_data():
    return True


@shared_task
def import_data():
    return True


@shared_task
def check_periodic_export():
    pass
