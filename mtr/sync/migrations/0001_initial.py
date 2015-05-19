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
            name='Field',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('position', models.PositiveIntegerField(blank=True, null=True, verbose_name='mtr.sync:position')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:name')),
                ('attribute', models.CharField(max_length=255, verbose_name='mtr.sync:model attribute')),
                ('skip', models.BooleanField(default=False, verbose_name='mtr.sync:skip')),
                ('update', models.BooleanField(default=True, verbose_name='mtr.sync:update')),
                ('update_value', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:value')),
                ('find', models.BooleanField(default=False, verbose_name='mtr.sync:find')),
                ('find_filter', models.CharField(blank=True, verbose_name='mtr.sync:filter type', choices=[('icontains', 'icontains'), ('contains', 'contains'), ('iexact', 'iexact'), ('exact', 'exact'), ('in', 'in'), ('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('lte', 'lte')], max_length=255)),
                ('converters', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:converters')),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'mtr.sync:field',
                'verbose_name_plural': 'mtr.sync:fields',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('position', models.PositiveIntegerField(blank=True, null=True, verbose_name='mtr.sync:position')),
                ('message', models.TextField(max_length=10000, verbose_name='mtr.sync:message')),
                ('step', models.PositiveSmallIntegerField(default=10, choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')], verbose_name='mtr.sync:step')),
                ('input_position', models.CharField(blank=True, max_length=10, verbose_name='mtr.sync:input position')),
                ('input_value', models.TextField(blank=True, verbose_name='mtr.sync:input value', max_length=60000, null=True)),
                ('type', models.PositiveSmallIntegerField(default=0, choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Info')], verbose_name='mtr.sync:type')),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'mtr.sync:message',
                'verbose_name_plural': 'mtr.sync:messages',
            },
            bases=(models.Model, mtr.sync.api.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('action', models.PositiveSmallIntegerField(db_index=True, choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], verbose_name='mtr.sync:action')),
                ('buffer_file', models.FileField(blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, verbose_name='mtr.sync:file')),
                ('status', models.PositiveSmallIntegerField(default=1, choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')], verbose_name='mtr.sync:status')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:started at')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='mtr.sync:completed at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('action', models.PositiveSmallIntegerField(db_index=True, choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], verbose_name='mtr.sync:action')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='mtr.sync:name')),
                ('start_col', models.CharField(blank=True, max_length=10, verbose_name='mtr.sync:start column')),
                ('start_row', models.PositiveIntegerField(blank=True, null=True, verbose_name='mtr.sync:start row')),
                ('end_col', models.CharField(blank=True, max_length=10, verbose_name='mtr.sync:end column')),
                ('end_row', models.PositiveIntegerField(blank=True, null=True, verbose_name='mtr.sync:end row')),
                ('model', models.CharField(blank=True, verbose_name='mtr.sync:model', choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Settings'), ('mtr_sync.field', 'Mtr_Sync | Field'), ('mtr_sync.report', 'Mtr_Sync | Report'), ('mtr_sync.message', 'Mtr_Sync | Message')], max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at')),
                ('processor', models.CharField(verbose_name='mtr.sync:format', default='XlsxProcessor', choices=[('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], max_length=255)),
                ('worksheet', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:worksheet page')),
                ('include_header', models.BooleanField(default=True, verbose_name='mtr.sync:include header')),
                ('filename', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:custom filename')),
                ('buffer_file', models.FileField(blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, verbose_name='mtr.sync:file')),
                ('dataset', models.CharField(blank=True, verbose_name='mtr.sync:dataset', choices=[('some_dataset', 'some description')], max_length=255)),
                ('data_action', models.CharField(blank=True, verbose_name='mtr.sync:data action', choices=[('create', 'mtr.sync:Create only'), ('update', 'mtr.sync:Update only'), ('update_or_create', 'mtr.sync:Update or create')], max_length=255)),
                ('filter_dataset', models.BooleanField(default=True, verbose_name='mtr.sync:filter custom dataset')),
                ('filter_querystring', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:querystring')),
                ('language', models.CharField(blank=True, verbose_name='mtr.sync:language', choices=[('de', 'German'), ('en', 'English')], max_length=255)),
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
            field=models.ForeignKey(related_name='reports', null=True, blank=True, verbose_name='mtr.sync:settings', to='mtr_sync.Settings'),
        ),
        migrations.AddField(
            model_name='message',
            name='report',
            field=models.ForeignKey(related_name='errors', to='mtr_sync.Report'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(related_name='fields', to='mtr_sync.Settings', verbose_name='mtr.sync:settings'),
        ),
    ]
