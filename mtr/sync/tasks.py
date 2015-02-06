from celery import shared_task


@shared_task
def export_data():
    return True