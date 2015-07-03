from functools import partial

from django.utils import formats
from django.utils.encoding import smart_text
from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse

from .helpers import themed, gettext_lazy as _
from .models import Report, Settings, Field, Message, Context, Sequence, \
    Replacer, ReplacerCategory
from .api.helpers import model_attributes
from .settings import SETTINGS
from .forms import SettingsAdminForm


class SyncAdminMixin(object):
    change_list_template = themed('admin/change_list.html', True)


class SyncTabularInlineMixin(object):
    template = themed('admin/edit_inline/tabular.html', True)


class SyncStackedInlineMixin(object):
    template = themed('admin/edit_inline/stacked.html', True)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('input_position', 'type', 'message', 'step', 'report')
    list_filter = ('type', 'report')


class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'action', 'status', 'settings',
        'started_at', 'completed_at', 'buffer_file_link')
    list_filter = (
        'action', 'status', 'settings', 'started_at', 'completed_at')
    search_fields = ('buffer_file',)
    readonly_fields = ('completed_at',)
    date_hierarchy = 'started_at'

    def buffer_file_link(self, obj):
        """Display download link"""

        return smart_text('<a href="{0}">{0}</a>').format(
            obj.get_absolute_url())

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
            if settings.model and not settings.edit_attributes:
                field = forms.ChoiceField(
                    label=field.label, required=field.required,
                    choices=model_attributes(settings))

        return field


class FieldInline(
        ObjectInlineMixin, AttributeChoicesInlineMixin, admin.StackedInline):
    model = Field
    extra = 0
    fields = (
        ('position', 'name', 'attribute'),
        ('skip', 'find', 'update'),
        ('find_filter', 'find_value'),
        ('set_filter', 'set_value'),
        ('converters', 'replacer_category'))
    sortable_field_name = 'position'


class ContextInline(admin.TabularInline):
    model = Context
    extra = 0


class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'action', 'model',
        'processor', 'created_at', 'latest_run_messages'
    )
    list_filter = ('sequence',)
    list_display_links = ('__str__', 'model')
    date_hierarchy = 'created_at'
    inlines = (FieldInline, ContextInline)
    actions = ['run', 'copy']
    fieldsets = (
        (None, {
            'fields': (
                ('model', 'action'),
                'processor',
                ('name', 'filename'),
                'buffer_file'
            )
        }),

        (_('Data settings'), {
            'fields': (
                ('dataset', 'data_action'),
                ('filter_dataset', 'filter_querystring')
            )
        }),

        (_('Worksheet settings'), {
            'fields': (
                ('start_row', 'end_row'),
                ('include_header', 'populate_from_file'),
                'worksheet',
            )
        }),

        (_('Language settings'), {
            'fields': (('language', 'hide_translation_fields'),)
        }),

        (_('Field settings'), {
            'fields': (
                ('create_fields', 'include_related', 'edit_attributes'),
            )
        }),
    )
    form = SettingsAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(SettingsAdmin, self).get_form(request, obj, **kwargs)
        action = request.GET.get('action', '')
        model = request.GET.get('model', '')
        filter_querystring = request.GET.get('filter', '')

        if action == 'export':
            form.INITIAL['action'] = 0
            form.INITIAL['create_fields'] = True
        elif action == 'import':
            form.INITIAL['action'] = 1
            form.INITIAL['populate_from_file'] = True

        form.INITIAL['model'] = model
        form.INITIAL['filter_querystring'] = filter_querystring

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
            _('Data synchronization started in background.'))
    run.short_description = _('Sync data')

    def copy(self, request, queryset):
        """Copy selected settings"""

        for settings in queryset:
            settings.create_copy()

        self.message_user(
            request,
            _('Copies successfully created'))
    copy.short_description = _('Create a copy of settings')

    def latest_run_messages(self, obj):
        report = obj.reports.first()
        if report:
            return smart_text('<a href="{}{}">{} - {}</a>').format(
                reverse('admin:mtr_sync_message_changelist'),
                '?report__id__exact={}'.format(report.id),
                formats.localize(report.started_at),
                report.get_status_display())
        return ''
    latest_run_messages.short_description = _('Latest run messages')
    latest_run_messages.allow_tags = True


class SequenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'buffer_file', 'latest_sync')
    filter_horizontal = ('settings', )
    actions = ('run',)

    def run(self, request, queryset):
        """Run action with selected settings"""

        for sequence in queryset:
            for settings in sequence.settings.all():
                settings.buffer_file = sequence.buffer_file
                settings.save()
                settings.run()

        self.message_user(
            request,
            _('Data synchronization started in background.'))
    run.short_description = _('Sync data')

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('name', 'settings')
        return tuple()

    def latest_sync(self, obj):
        report = obj.settings.first().reports.first()
        if report:
            return smart_text('<a href="{}{}">{} - {}</a>').format(
                reverse('admin:mtr_sync_message_changelist'),
                '?report__id__exact={}'.format(report.id),
                formats.localize(report.started_at),
                report.get_status_display())
        return ''
    latest_sync.short_description = _('Latest sync')
    latest_sync.allow_tags = True


class ReplacerCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']


class ReplacerAdmin(admin.ModelAdmin):
    list_display = ['id', 'value', 'change_to', 'regex', 'category']
    list_editable = ['value', 'change_to', 'regex', 'category']


if SETTINGS['REGISTER_IN_ADMIN']:
    admin.site.register(Report, ReportAdmin)
    admin.site.register(Message, MessageAdmin)
    admin.site.register(Settings, SettingsAdmin)
    admin.site.register(Sequence, SequenceAdmin)
    admin.site.register(Replacer, ReplacerAdmin)
    admin.site.register(ReplacerCategory, ReplacerCategoryAdmin)
