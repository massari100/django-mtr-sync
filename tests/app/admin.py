from random import shuffle, choice

from django.contrib import admin
from django.utils.six.moves import range

from .models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'surname', 'security_level', 'gender')
    # list_filter = ('name', 'surname', 'security_level', 'gender')

    actions = ['copy_1000']

    def copy_1000(self, request, queryset):
        for item in queryset.all():
            for i in range(1000):
                name = list(item.name)
                shuffle(name)
                name = ''.join(name)

                surname = list(item.surname)
                shuffle(surname)
                surname = ''.join(surname)

                item.__class__.objects.create(
                    name=name,
                    surname=surname,
                    gender=choice(['M', 'F']),
                    security_level=choice(range(100))
                )
    copy_1000.short_description = 'Copy 1000 objects with random data'


admin.site.register(Person, PersonAdmin)
