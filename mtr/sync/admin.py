from __future__ import unicode_literals

import os

from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from .models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = (
        'started_at', 'action', 'status', 'completed_at', 'buffer_file_link')
    list_filter = ('action', 'status', 'started_at', 'completed_at')
    search_fields = ('buffer_file',)
    readonly_fields = ('completed_at',)
    date_hierarchy = 'started_at'

    def buffer_file_link(self, obj):
        """Display download link"""

        return '<a href="{}">{}</a>'.format(
            obj.get_absolute_url(), os.path.basename(obj.buffer_file.name))

    buffer_file_link.allow_tags = True
    buffer_file_link.short_description = _(
        'mtr.sync:Link to file')

admin.site.register(Log, LogAdmin)
