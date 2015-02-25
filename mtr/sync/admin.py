import os

from functools import partial

from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django import forms

from .models import Report, Settings, Field, FilterParams, Filter, Error
from .api import manager


class ErrorInline(admin.TabularInline):
    model = Error
    extra = 0


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


class FilterInline(admin.TabularInline):
    model = FilterParams
    extra = 0


class FilterAdmin(admin.ModelAdmin):
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
                choices=manager.model_attributes(settings))

    class Meta:
        exclude = []
        model = Field


class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'attribute', 'settings')
    list_filter = ('settings',)
    inlines = (FilterInline,)
    form = FieldForm


class FieldInline(admin.TabularInline):
    model = Field
    extra = 0

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
                choices=manager.model_attributes(settings))

        return field


class SettingsForm(forms.ModelForm):

    create_fields = forms.BooleanField(
        label=_('mtr.sync:Create settings for fields'),
        initial=False, required=False)

    def save(self, commit=True):
        create_fields = self.cleaned_data.get('create_fields', False)

        settings = super(SettingsForm, self).save(commit=commit)
        settings.save()

        if create_fields:
            settings.create_default_fields()

        return settings

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

admin.site.register(Report, ReportAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Filter, FilterAdmin)
