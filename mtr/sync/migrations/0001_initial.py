# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mtr.sync.settings
import mtr.sync.api.exceptions


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', null=True, blank=True)),
                ('message', models.TextField(max_length=10000, verbose_name='mtr.sync:message')),
                ('step', models.PositiveSmallIntegerField(default=10, verbose_name='mtr.sync:step', choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')])),
                ('input_position', models.CharField(max_length=10, verbose_name='mtr.sync:input position', blank=True)),
                ('input_value', models.TextField(max_length=60000, verbose_name='mtr.sync:input value', null=True, blank=True)),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'mtr.sync:error',
                'verbose_name_plural': 'mtr.sync:errors',
            },
            bases=(models.Model, mtr.sync.api.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', null=True, blank=True)),
                ('name', models.CharField(max_length=255, verbose_name='mtr.sync:name', blank=True)),
                ('attribute', models.CharField(max_length=255, verbose_name='mtr.sync:model attribute')),
                ('skip', models.BooleanField(default=False, verbose_name='mtr.sync:skip')),
                ('update', models.BooleanField(default=True, verbose_name='mtr.sync:update')),
                ('update_value', models.CharField(max_length=255, verbose_name='mtr.sync:value', blank=True)),
                ('find', models.BooleanField(default=False, verbose_name='mtr.sync:find')),
                ('find_filter', models.CharField(max_length=255, verbose_name='mtr.sync:filter type', blank=True, choices=[('icontains', 'icontains'), ('contains', 'contains'), ('iexact', 'iexact'), ('exact', 'exact'), ('in', 'in'), ('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('lte', 'lte')])),
                ('converters', models.CharField(max_length=255, verbose_name='mtr.sync:converters')),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'mtr.sync:field',
                'verbose_name_plural': 'mtr.sync:fields',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(verbose_name='mtr.sync:action', db_index=True, choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')])),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', db_index=True, blank=True, upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name='mtr.sync:status', choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')])),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:started at')),
                ('completed_at', models.DateTimeField(verbose_name='mtr.sync:completed at', null=True, blank=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'mtr.sync:report',
                'verbose_name_plural': 'mtr.sync:reports',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(verbose_name='mtr.sync:action', db_index=True, choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')])),
                ('name', models.CharField(max_length=100, verbose_name='mtr.sync:name', blank=True)),
                ('start_col', models.CharField(max_length=10, verbose_name='mtr.sync:start column', blank=True)),
                ('start_row', models.PositiveIntegerField(verbose_name='mtr.sync:start row', null=True, blank=True)),
                ('end_col', models.CharField(max_length=10, verbose_name='mtr.sync:end column', blank=True)),
                ('end_row', models.PositiveIntegerField(verbose_name='mtr.sync:end row', null=True, blank=True)),
                ('model', models.CharField(max_length=255, verbose_name='mtr.sync:model', blank=True, choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Settings'), ('mtr_sync.field', 'Mtr_Sync | Field'), ('mtr_sync.report', 'Mtr_Sync | Report'), ('mtr_sync.error', 'Mtr_Sync | Error')])),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:created at')),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
                ('processor', models.CharField(default='XlsxProcessor', max_length=255, choices=[('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], verbose_name='mtr.sync:format')),
                ('worksheet', models.CharField(max_length=255, verbose_name='mtr.sync:worksheet page', blank=True)),
                ('include_header', models.BooleanField(default=True, verbose_name='mtr.sync:include header')),
                ('filename', models.CharField(max_length=255, verbose_name='mtr.sync:custom filename', blank=True)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', db_index=True, blank=True, upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('dataset', models.CharField(max_length=255, verbose_name='mtr.sync:dataset', blank=True, choices=[('some_dataset', 'some description')])),
                ('data_action', models.CharField(max_length=255, verbose_name='mtr.sync:data action', blank=True, choices=[('create', 'mtr.sync:Create only'), ('update', 'mtr.sync:Update only')])),
                ('filter_dataset', models.BooleanField(default=True, verbose_name='mtr.sync:filter custom dataset')),
                ('filter_querystring', models.CharField(max_length=255, verbose_name='mtr.sync:querystring', blank=True)),
                ('language', models.CharField(max_length=255, verbose_name='mtr.sync:language', blank=True, choices=[('de', 'German'), ('en', 'English')])),
                ('hide_translation_fields', models.BooleanField(default=True, verbose_name='mtr.sync:Hide translation prefixed fields')),
                ('create_fields', models.BooleanField(default=True, verbose_name='mtr.sync:Create settings for fields')),
                ('populate_from_file', models.BooleanField(default=False, verbose_name='mtr.sync:Populate settings from file')),
                ('run_after_save', models.BooleanField(default=False, verbose_name='mtr.sync:Start action after saving')),
                ('include_related', models.BooleanField(default=True, verbose_name='mtr.sync:Include related fields')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'mtr.sync:settings',
                'verbose_name_plural': 'mtr.sync:settings',
            },
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(null=True, to='mtr_sync.Settings', verbose_name='mtr.sync:settings', blank=True, related_name='reports'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(related_name='fields', to='mtr_sync.Settings', verbose_name='mtr.sync:settings'),
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(related_name='errors', to='mtr_sync.Report'),
        ),
    ]
