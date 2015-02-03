from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from .models import LogEntry


@staff_member_required
def dashboard(request):
    context = {
        'last_imported': LogEntry.import_objects.all()[:10],
        'last_exported': LogEntry.export_objects.all()[:10]
    }

    return render(request, 'mtr/sync/dashboard.html', context)
