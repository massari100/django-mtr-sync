# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mtr.sync.settings


class Migration(migrations.Migration):

    dependencies = [
        ('mtr_sync', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='error',
            options={'verbose_name_plural': 'mtr.sync:errors', 'verbose_name': 'mtr.sync:error', 'ordering': ('position',)},
        ),
        migrations.AlterModelOptions(
            name='field',
            options={'verbose_name_plural': 'mtr.sync:fields', 'verbose_name': 'mtr.sync:field', 'ordering': ('position',)},
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'verbose_name_plural': 'mtr.sync:reports', 'verbose_name': 'mtr.sync:report', 'ordering': ('-id',)},
        ),
        migrations.AlterModelOptions(
            name='settings',
            options={'verbose_name_plural': 'mtr.sync:settings', 'verbose_name': 'mtr.sync:settings', 'ordering': ('-id',)},
        ),
        migrations.AlterField(
            model_name='error',
            name='input_position',
            field=models.CharField(max_length=10, blank=True, verbose_name='mtr.sync:input position'),
        ),
        migrations.AlterField(
            model_name='error',
            name='input_value',
            field=models.TextField(max_length=60000, blank=True, verbose_name='mtr.sync:input value', null=True),
        ),
        migrations.AlterField(
            model_name='error',
            name='message',
            field=models.TextField(max_length=10000, verbose_name='mtr.sync:message'),
        ),
        migrations.AlterField(
            model_name='error',
            name='position',
            field=models.PositiveIntegerField(blank=True, verbose_name='mtr.sync:position', null=True),
        ),
        migrations.AlterField(
            model_name='error',
            name='step',
            field=models.PositiveSmallIntegerField(default=10, choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')], verbose_name='mtr.sync:step'),
        ),
        migrations.AlterField(
            model_name='field',
            name='attribute',
            field=models.CharField(max_length=255, verbose_name='mtr.sync:model attribute'),
        ),
        migrations.AlterField(
            model_name='field',
            name='converters',
            field=models.CharField(max_length=255, verbose_name='mtr.sync:converters'),
        ),
        migrations.AlterField(
            model_name='field',
            name='find',
            field=models.BooleanField(default=False, verbose_name='mtr.sync:find'),
        ),
        migrations.AlterField(
            model_name='field',
            name='find_filter',
            field=models.CharField(max_length=255, blank=True, choices=[('icontains', 'icontains'), ('contains', 'contains'), ('iexact', 'iexact'), ('exact', 'exact'), ('in', 'in'), ('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('lte', 'lte')], verbose_name='mtr.sync:filter type'),
        ),
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.CharField(max_length=255, blank=True, verbose_name='mtr.sync:name'),
        ),
        migrations.AlterField(
            model_name='field',
            name='position',
            field=models.PositiveIntegerField(blank=True, verbose_name='mtr.sync:position', null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(related_name='fields', verbose_name='mtr.sync:settings', to='mtr_sync.Settings'),
        ),
        migrations.AlterField(
            model_name='field',
            name='skip',
            field=models.BooleanField(default=False, verbose_name='mtr.sync:skip'),
        ),
        migrations.AlterField(
            model_name='field',
            name='update',
            field=models.BooleanField(default=True, verbose_name='mtr.sync:update'),
        ),
        migrations.AlterField(
            model_name='field',
            name='update_value',
            field=models.CharField(max_length=255, blank=True, verbose_name='mtr.sync:value'),
        ),
        migrations.AlterField(
            model_name='report',
            name='action',
            field=models.PositiveSmallIntegerField(choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], db_index=True, verbose_name='mtr.sync:action'),
        ),
        migrations.AlterField(
            model_name='report',
            name='buffer_file',
            field=models.FileField(blank=True, db_index=True, verbose_name='mtr.sync:file', upload_to=mtr.sync.settings.get_buffer_file_path),
        ),
        migrations.AlterField(
            model_name='report',
            name='completed_at',
            field=models.DateTimeField(blank=True, verbose_name='mtr.sync:completed at', null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(null=True, related_name='reports', blank=True, verbose_name='mtr.sync:settings', to='mtr_sync.Settings'),
        ),
        migrations.AlterField(
            model_name='report',
            name='started_at',
            field=models.DateTimeField(verbose_name='mtr.sync:started at', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.PositiveSmallIntegerField(default=1, choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')], verbose_name='mtr.sync:status'),
        ),
        migrations.AlterField(
            model_name='report',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='action',
            field=models.PositiveSmallIntegerField(choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], db_index=True, verbose_name='mtr.sync:action'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='buffer_file',
            field=models.FileField(blank=True, db_index=True, verbose_name='mtr.sync:file', upload_to=mtr.sync.settings.get_buffer_file_path),
        ),
        migrations.AlterField(
            model_name='settings',
            name='create_fields',
            field=models.BooleanField(default=True, verbose_name='mtr.sync:Create settings for fields'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='created_at',
            field=models.DateTimeField(verbose_name='mtr.sync:created at', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='settings',
            name='data_action',
            field=models.CharField(max_length=255, blank=True, choices=[('create', 'mtr.sync:Create only'), ('update', 'mtr.sync:Update only'), ('update_or_create', 'mtr.sync:Update or create')], verbose_name='mtr.sync:data action'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='dataset',
            field=models.CharField(max_length=255, blank=True, choices=[('some_dataset', 'some description')], verbose_name='mtr.sync:dataset'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='end_col',
            field=models.CharField(max_length=10, blank=True, verbose_name='mtr.sync:end column'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='end_row',
            field=models.PositiveIntegerField(blank=True, verbose_name='mtr.sync:end row', null=True),
        ),
        migrations.AlterField(
            model_name='settings',
            name='filename',
            field=models.CharField(max_length=255, blank=True, verbose_name='mtr.sync:custom filename'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='filter_dataset',
            field=models.BooleanField(default=True, verbose_name='mtr.sync:filter custom dataset'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='filter_querystring',
            field=models.CharField(max_length=255, blank=True, verbose_name='mtr.sync:querystring'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='hide_translation_fields',
            field=models.BooleanField(default=True, verbose_name='mtr.sync:Hide translation prefixed fields'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='include_header',
            field=models.BooleanField(default=True, verbose_name='mtr.sync:include header'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='include_related',
            field=models.BooleanField(default=True, verbose_name='mtr.sync:Include related fields'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='language',
            field=models.CharField(max_length=255, blank=True, choices=[('de', 'German'), ('en', 'English')], verbose_name='mtr.sync:language'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='model',
            field=models.CharField(max_length=255, blank=True, choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Settings'), ('mtr_sync.field', 'Mtr_Sync | Field'), ('mtr_sync.report', 'Mtr_Sync | Report'), ('mtr_sync.error', 'Mtr_Sync | Error')], verbose_name='mtr.sync:model'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='name',
            field=models.CharField(max_length=100, blank=True, verbose_name='mtr.sync:name'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='populate_from_file',
            field=models.BooleanField(default=False, verbose_name='mtr.sync:Populate settings from file'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='processor',
            field=models.CharField(default='XlsxProcessor', max_length=255, choices=[('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], verbose_name='mtr.sync:format'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='run_after_save',
            field=models.BooleanField(default=False, verbose_name='mtr.sync:Start action after saving'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='start_col',
            field=models.CharField(max_length=10, blank=True, verbose_name='mtr.sync:start column'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='start_row',
            field=models.PositiveIntegerField(blank=True, verbose_name='mtr.sync:start row', null=True),
        ),
        migrations.AlterField(
            model_name='settings',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='worksheet',
            field=models.CharField(max_length=255, blank=True, verbose_name='mtr.sync:worksheet page'),
        ),
    ]
