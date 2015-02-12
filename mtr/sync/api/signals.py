from django.dispatch import Signal

export_started = Signal(['processor'])
export_completed = Signal(['report', 'completed_at', 'path'])

import_started = Signal([])
import_completed = Signal(['report', 'completed_at'])
