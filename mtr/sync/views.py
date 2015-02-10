from django.contrib.admin.views.decorators import staff_member_required

from .models import Report
from .helpers import render_to
from .tasks import export_data


@staff_member_required
@render_to('dashboard.html')
def dashboard(request):
    context = {
        'last_imported': Report.import_objects.all()[:10],
        'last_exported': Report.export_objects.all()[:10]
    }

    #export_data.apply_async()

    return context


def import_upload(request):
    pass


def import_settings(request):
    pass


def import_result(request):
    pass
