import os

from functools import partial

from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django import forms

from .helpers import themed
from .models import Report, Settings, Field, Error
from .api.helpers import model_attributes
from .settings import REGISTER_IN_ADMIN


class SyncAdminMixin(object):
    change_list_template = themed('admin/change_list.html')


class SyncTabularInlineMixin(object):
    template = themed('admin/edit_inline/tabular.html')


class SyncStackedInlineMixin(object):
    template = themed('admin/edit_inline/stacked.html')


class ErrorInline(admin.TabularInline):
    model = Error
    extra = 0
    readonly_fields = (
        'position', 'message', 'step', 'input_position', 'input_value')


class ReportAdmin(admin.ModelAdmin):
    inlines = (ErrorInline,)
    list_display = (
        'action', 'status', 'started_at', 'completed_at', 'buffer_file_link')
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


class ObjectInlineMixin(object):

    def get_formset(self, request, obj=None, **kwargs):
        """Pass parent object to inline form"""

        kwargs['formfield_callback'] = partial(
            self.formfield_for_dbfield, request=request, obj=obj)
        return super(ObjectInlineMixin, self) \
            .get_formset(request, obj, **kwargs)


class AttributeChoicesInlineMixin(object):

    def formfield_for_dbfield(self, db_field, **kwargs):
        """Replace inline attribute field to selectbox with choices"""

        settings = kwargs.pop('obj')

        field = super(
            AttributeChoicesInlineMixin, self
            ).formfield_for_dbfield(db_field, **kwargs)

        if db_field.name == 'attribute':
            if settings.action != settings.IMPORT and settings.model:
                field = forms.ChoiceField(
                    label=field.label, required=field.required,
                    choices=model_attributes(settings))

        return field


class FieldInline(
        ObjectInlineMixin, AttributeChoicesInlineMixin, admin.TabularInline):
    model = Field
    extra = 0
    fields = ('skip', 'position', 'name', 'attribute', 'converters')


class SettingsForm(forms.ModelForm):
    INITIAL = {}

    def __init__(self, *args, **kwargs):
        if kwargs.get('initial', None):
            kwargs['initial'].update(self.INITIAL)

        super(SettingsForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        settings = super(SettingsForm, self).save(commit=commit)

        # BUG: why always commit=False

        settings.save()

        if settings.create_fields:
            settings.create_default_fields()
            settings.create_fields = False

        if settings.action == settings.IMPORT \
                and settings.buffer_file and settings.populate_from_file:
            settings.populate_from_buffer_file()
            settings.populate_from_file = False

        settings.save()

        return settings

    class Meta:
        exclude = []
        model = Settings


class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'action', 'model',
        'processor', 'created_at', 'updated_at'
    )
    list_display_links = ('id', 'name', 'model')
    date_hierarchy = 'created_at'
    inlines = (FieldInline,)
    actions = ['run']
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'language'),
                ('action', 'processor'),
                ('start_col', 'end_col'), ('start_row', 'end_row'),
                ('model', 'dataset', 'data_action'),
                ('filename', 'worksheet', 'include_header'),
                ('filter_querystring',)
            )
        }),
        (_('mtr.sync:Additional options'),     {
            'fields': (
                ('create_fields', 'populate_from_file'),
                ('language_attributes', 'filter_dataset'),)
        })
    )
    form = SettingsForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(SettingsAdmin, self).get_form(request, obj, **kwargs)
        action = request.GET.get('action', '')
        model = request.GET.get('model', '')
        filter_querystring = request.GET.get('filter', '')

        # TODO: create initial fields automaticaly
        # TODO: modify attributes by simple custom widget

        if action == 'export':
            form.INITIAL['action'] = 0
            form.INITIAL['create_fields'] = True
        elif action == 'import':
            form.INITIAL['action'] = 1
            form.INITIAL['populate_from_file'] = True

        form.INITIAL['model'] = model
        form.INITIAL['filter_querystring'] = filter_querystring

        # form.INITIAL['fields'] = [
        #     {'order': 0},
        # ]

        # print(self.inlines)

        return form

    def get_inline_instances(self, request, obj=None):
        """Show inlines only in saved models"""

        if obj:
            inlines = super(
                SettingsAdmin, self).get_inline_instances(request, obj)
            return inlines
        else:
            return []

    def run(self, request, queryset):
        """Run action with selected settings"""

        for settings in queryset:
            settings.run()

            self.message_user(
                request,
                _('mtr.sync:Data synchronization started in background.'))

    run.short_description = _('mtr.sync:Sync data')

if REGISTER_IN_ADMIN():
    admin.site.register(Report, ReportAdmin)
    admin.site.register(Settings, SettingsAdmin)
