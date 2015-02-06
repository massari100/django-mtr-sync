from django.contrib.admin.views.decorators import staff_member_required

from .models import LogEntry
from .helpers import render_to
from .tasks import export_data


@staff_member_required
@render_to('dashboard.html')
def dashboard(request):
    context = {
        'last_imported': LogEntry.import_objects.all()[:10],
        'last_exported': LogEntry.export_objects.all()[:10]
    }

    # test celery in-memory apply_async, gives error, with apply() all OK
    export_data.apply_async()

    return context
