import django

from django.contrib import admin

if django.get_version() >= '1.7':
    from mtr.sync.admin import ImportExportAdminMixin
else:
    from mtr_sync.admin import ImportExportAdminMixin

from .models import Person, Office, Tag


class PersonAdmin(ImportExportAdminMixin, admin.ModelAdmin):
    list_display = (
        'name', 'surname', 'security_level', 'gender')

    actions = ['copy_100']

    def copy_100(self, request, queryset):
        for item in queryset.all():
            item.populate()
    copy_100.short_description = 'Copy 100 objects with random data'


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('office', 'address')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Person, PersonAdmin)
admin.site.register(Office, OfficeAdmin)
admin.site.register(Tag, TagAdmin)
