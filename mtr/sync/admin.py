import os

from functools import partial

from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django import forms

from .helpers import themed
from .models import Report, Settings, Field, Error, Filter
from .api.helpers import model_attributes
from .settings import REGISTER_IN_ADMIN


class ImportExportAdminMixin(object):
    change_list_template = themed('admin/change_list.html')


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


class FieldForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """Replace default attribute field to selectbox with choices"""

        super(FieldForm, self).__init__(*args, **kwargs)

        settings = self.initial.get('settings', None)
        if settings:
            for av_settings in self.fields['settings']._queryset:
                if av_settings.id == settings:
                    settings = av_settings
                    break

            if settings.action != settings.IMPORT and \
                    settings.model:

                field = self.fields['attribute']
                self.fields['attribute'] = forms.ChoiceField(
                    label=field.label, required=field.required,
                    choices=model_attributes(settings))

    class Meta:
        fields = ['skip', 'name', 'attribute', 'converters']
        exclude = []
        model = Field


class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'attribute', 'converters', 'settings')
    list_filter = ('settings',)
    form = FieldForm


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


class FilterInline(
        ObjectInlineMixin, AttributeChoicesInlineMixin, admin.TabularInline):
    model = Filter
    extra = 0
    fields = ('position', 'attribute', 'filter_type', 'value')


class SettingsForm(forms.ModelForm):
    INITIAL = {}

    create_fields = forms.BooleanField(
        label=_('mtr.sync:Create settings for fields'),
        initial=False, required=False)

    populate_from_file = forms.BooleanField(
        label=_('mtr.sync:Populate settings from file'),
        initial=False, required=False)

    translation_attributes = forms.BooleanField(
        label=_('mtr.sync:Hide translation prefixed fields'),
        initial=True, required=False)    

    def __init__(self, *args, **kwargs):
        if kwargs.get('initial', None):
            kwargs['initial'].update(self.INITIAL)

        super(SettingsForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        create_fields = self.cleaned_data.get('create_fields', False)
        populate_from_file = self.cleaned_data.get('populate_from_file', False)
        translation_attributes = self.cleaned_data.get(
            'translation_attributes', False)

        settings = super(SettingsForm, self).save(commit=commit)

        # BUG: why always commit=False

        settings.save()

        if create_fields:
            settings.create_default_fields()

        if settings.action == settings.IMPORT \
                and settings.buffer_file and populate_from_file:
            settings.populate_from_buffer_file()

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
    inlines = (FieldInline, FilterInline)
    actions = ['run']
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'language'),
                ('action', 'processor'),
                ('start_col', 'end_col'), ('start_row', 'end_row'),
                ('model', 'dataset', 'data_action'),
                ('filename', 'worksheet', 'include_header'),
            )
        }),
        (_('mtr.sync:Additional options'),     {
            'fields': (('create_fields', 'populate_from_file'), 
                ('translation_attributes', 'filter_dataset'),)
        })
    )
    form = SettingsForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(SettingsAdmin, self).get_form(request, obj, **kwargs)
        action = request.GET.get('action', '')
        model = request.GET.get('model', '')

        # TODO: create initial fields automaticaly
        # TODO: modify attributes by simple custom widget

        if action == 'export':
            form.INITIAL['action'] = 0
            form.INITIAL['create_fields'] = True
        elif action == 'import':
            form.INITIAL['action'] = 1
            form.INITIAL['populate_from_file'] = True
            form.INITIAL['create_fields'] = False

        form.INITIAL['model'] = model

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
    admin.site.register(Field, FieldAdmin)
