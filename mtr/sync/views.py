from django.contrib.admin.views.decorators import staff_member_required

from .models import Report, Settings
from .helpers import render_to


@staff_member_required
@render_to('dashboard.html')
def dashboard(request):
    context = {
        'last_reports': Report.objects.all()[:10],
        'new_settings': Settings.objects.all()[:10]
    }

    return context


@staff_member_required
@render_to('export.html')
def export(request):
    return {}


def import_upload(request):
    pass


def import_settings(request):
    pass


def import_result(request):
    pass
