import os

from functools import partial

from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.core.urlresolvers import reverse
from django import forms

from .models import Report, Settings, Field, ValueProcessorParams, \
    ValueProcessor, Error
from .api import manager
from .api.helpers import model_attributes, queryset_choices
from .settings import REGISTER_AT_ADMIN


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


class ValueProcessorParamsInline(admin.TabularInline):
    model = ValueProcessorParams
    extra = 0


class ValueProcessorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


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

            self.fields['attribute'] = forms.ChoiceField(
                label=self.fields['attribute'].label,
                choices=model_attributes(settings))

    class Meta:
        exclude = []
        model = Field


class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'attribute', 'settings')
    list_filter = ('settings',)
    inlines = (ValueProcessorParamsInline,)
    form = FieldForm


class FieldInline(admin.TabularInline):
    model = Field
    extra = 0
    readonly_fields = ('processors_list',)
    fields = (
        'position', 'name', 'attribute', 'processors_list', 'skip')

    def get_formset(self, request, obj=None, **kwargs):
        """Pass parent object to inline form"""

        kwargs['formfield_callback'] = partial(
            self.formfield_for_dbfield, request=request, obj=obj)
        return super(FieldInline, self).get_formset(request, obj, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        """Replace inline attribute field to selectbox with choices"""

        settings = kwargs.pop('obj')

        field = super(
            FieldInline, self).formfield_for_dbfield(db_field, **kwargs)

        if db_field.name == 'attribute':
            field = forms.ChoiceField(
                label=field.label,
                choices=model_attributes(settings))

        return field

    def processors_list(self, obj):
        processors = obj.processors.all()
        result = []
        if processors:
            result = ["<ul>"]
            for processor in processors:
                result.append("<li>{}</li>".format(processor.label))
        else:
            # TODO: fix translation join
            result.append("No value processors selected<br>")
        result.append('<a href="{}">{}</a>'.format(
            reverse('admin:mtrsync_field_change', args=[obj.id]),
            'Add processors'))

        return ''.join(result)

    processors_list.short_description = _('mtr.sync:Processors')
    processors_list.allow_tags = True


class SettingsForm(forms.ModelForm):

    create_fields = forms.BooleanField(
        label=_('mtr.sync:Create settings for fields'),
        initial=False, required=False)

    populate = forms.BooleanField(
        label=_('mtr.sync:Populate settings from file'),
        initial=False, required=False)

    def save(self, commit=True):
        create_fields = self.cleaned_data.get('create_fields', False)
        populate = self.cleaned_data.get('populate', False)

        settings = super(SettingsForm, self).save(commit=commit)

        settings.save()

        if create_fields:
            settings.create_default_fields()

        if settings.action == settings.IMPORT \
                and settings.buffer_file and populate:
            settings.populate_from_buffer_file()

        settings.save()

        return settings

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.fields['queryset'] = forms.ChoiceField(
                label=self.fields['queryset'].label,
                choices=queryset_choices(self.instance),
                required=self.fields['queryset'].required)

    class Meta:
        exclude = []
        model = Settings


class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'action', 'main_model',
        'processor', 'created_at', 'updated_at'
    )
    date_hierarchy = 'created_at'
    inlines = (FieldInline,)
    actions = ['run']
    form = SettingsForm

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

if REGISTER_AT_ADMIN():
    admin.site.register(Report, ReportAdmin)
    admin.site.register(Settings, SettingsAdmin)
    admin.site.register(Field, FieldAdmin)
    admin.site.register(ValueProcessor, ValueProcessorAdmin)
