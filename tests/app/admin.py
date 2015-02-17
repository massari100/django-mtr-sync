from django.contrib import admin

from .models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'surname', 'security_level', 'gender')

    actions = ['copy_100']

    def copy_100(self, request, queryset):
        for item in queryset.all():
            item.populate()
    copy_100.short_description = 'Copy 100 objects with random data'


admin.site.register(Person, PersonAdmin)
