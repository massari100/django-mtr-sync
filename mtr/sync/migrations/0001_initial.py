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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('position', models.PositiveIntegerField(blank=True, null=True, verbose_name='mtr.sync:position')),
                ('message', models.TextField(max_length=10000, verbose_name='mtr.sync:message')),
                ('step', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')], default=10, verbose_name='mtr.sync:step')),
                ('input_position', models.CharField(blank=True, max_length=10, verbose_name='mtr.sync:input position')),
                ('input_value', models.TextField(blank=True, max_length=60000, null=True, verbose_name='mtr.sync:input value')),
            ],
            options={
                'verbose_name': 'mtr.sync:error',
                'verbose_name_plural': 'mtr.sync:errors',
                'ordering': ('position',),
            },
            bases=(models.Model, mtr.sync.api.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('position', models.PositiveIntegerField(blank=True, null=True, verbose_name='mtr.sync:position')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:name')),
                ('attribute', models.CharField(max_length=255, verbose_name='mtr.sync:model attribute')),
                ('skip', models.BooleanField(default=False, verbose_name='mtr.sync:skip')),
                ('converters', models.CharField(max_length=255, verbose_name='mtr.sync:converters')),
            ],
            options={
                'verbose_name': 'mtr.sync:field',
                'verbose_name_plural': 'mtr.sync:fields',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('position', models.PositiveIntegerField(blank=True, null=True, verbose_name='mtr.sync:position')),
                ('attribute', models.CharField(max_length=255, verbose_name='mtr.sync:model attribute')),
                ('filter_type', models.CharField(max_length=255, verbose_name='mtr.sync:filter type')),
                ('value', models.CharField(max_length=255, verbose_name='mtr.sync:value')),
            ],
            options={
                'verbose_name': 'mtr.sync:filter',
                'verbose_name_plural': 'mtr.sync:filters',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], db_index=True, verbose_name='mtr.sync:action')),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, blank=True, db_index=True, verbose_name='mtr.sync:file')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')], default=1, verbose_name='mtr.sync:status')),
                ('started_at', models.DateTimeField(verbose_name='mtr.sync:started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='mtr.sync:completed at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at')),
            ],
            options={
                'verbose_name': 'mtr.sync:report',
                'verbose_name_plural': 'mtr.sync:reports',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], db_index=True, verbose_name='mtr.sync:action')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='mtr.sync:name')),
                ('start_col', models.CharField(blank=True, max_length=10, verbose_name='mtr.sync:start column')),
                ('start_row', models.PositiveIntegerField(blank=True, null=True, verbose_name='mtr.sync:start row')),
                ('end_col', models.CharField(blank=True, max_length=10, verbose_name='mtr.sync:end column')),
                ('end_row', models.PositiveIntegerField(blank=True, null=True, verbose_name='mtr.sync:end row')),
                ('model', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:model', choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Mtr.Sync:Settings'), ('mtr_sync.field', 'Mtr_Sync | Mtr.Sync:Field'), ('mtr_sync.filter', 'Mtr_Sync | Mtr.Sync:Filter'), ('mtr_sync.report', 'Mtr_Sync | Mtr.Sync:Report'), ('mtr_sync.error', 'Mtr_Sync | Mtr.Sync:Error')])),
                ('created_at', models.DateTimeField(verbose_name='mtr.sync:created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at')),
                ('processor', models.CharField(choices=[('XlsProcessor', '.xls | mtr.sync:Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | mtr.sync:Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | mtr.sync:ODF Spreadsheet'), ('CsvProcessor', '.csv | mtr.sync:CSV')], max_length=255, verbose_name='mtr.sync:format')),
                ('worksheet', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:worksheet page')),
                ('include_header', models.BooleanField(default=True, verbose_name='mtr.sync:include header')),
                ('filename', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:custom filename')),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, blank=True, db_index=True, verbose_name='mtr.sync:file')),
                ('dataset', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:dataset', choices=[('some_dataset', 'some description')])),
                ('filter_dataset', models.BooleanField(default=True, verbose_name='mtr.sync:filter custom dataset')),
                ('data_action', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:data action', choices=[('create', 'mtr.sync:Create instances without filter')])),
                ('language', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:language', choices=[('de', 'German'), ('en', 'English')])),
                ('language_attributes', models.BooleanField(default=True, verbose_name='mtr.sync:Hide translation prefixed fields')),
                ('create_fields', models.BooleanField(default=True, verbose_name='mtr.sync:Create settings for fields')),
                ('populate_from_file', models.BooleanField(default=False, verbose_name='mtr.sync:Populate settings from file')),
            ],
            options={
                'verbose_name': 'mtr.sync:settings',
                'verbose_name_plural': 'mtr.sync:settings',
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(blank=True, null=True, verbose_name='mtr.sync:settings', to='mtr_sync.Settings', related_name='reports'),
        ),
        migrations.AddField(
            model_name='filter',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', to='mtr_sync.Settings', related_name='filters'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', to='mtr_sync.Settings', related_name='fields'),
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(to='mtr_sync.Report', related_name='errors'),
        ),
    ]
