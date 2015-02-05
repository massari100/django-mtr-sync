from django.contrib.admin.views.decorators import staff_member_required

from .models import LogEntry
from .helpers import render_to


@staff_member_required
@render_to('dashboard.html')
def dashboard(request):
    context = {
        'last_imported': LogEntry.import_objects.all()[:10],
        'last_exported': LogEntry.export_objects.all()[:10]
    }

    return context
