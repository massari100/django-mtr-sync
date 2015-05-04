# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mtr.sync.api.exceptions
import mtr.sync.settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', null=True, blank=True)),
                ('message', models.TextField(verbose_name='mtr.sync:message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(verbose_name='mtr.sync:step', default=10, choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')])),
                ('input_position', models.CharField(verbose_name='mtr.sync:input position', max_length=10, blank=True)),
                ('input_value', models.TextField(verbose_name='mtr.sync:input value', null=True, max_length=60000, blank=True)),
            ],
            options={
                'verbose_name': 'mtr.sync:error',
                'ordering': ('position',),
                'verbose_name_plural': 'mtr.sync:errors',
            },
            bases=(models.Model, mtr.sync.api.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', null=True, blank=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=255, blank=True)),
                ('attribute', models.CharField(verbose_name='mtr.sync:model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='mtr.sync:skip', default=False)),
                ('converters', models.CharField(verbose_name='mtr.sync:converters', max_length=255)),
            ],
            options={
                'verbose_name': 'mtr.sync:field',
                'ordering': ('position',),
                'verbose_name_plural': 'mtr.sync:fields',
            },
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', null=True, blank=True)),
                ('attribute', models.CharField(verbose_name='mtr.sync:model attribute', max_length=255)),
                ('filter_type', models.CharField(verbose_name='mtr.sync:filter type', max_length=255)),
                ('value', models.CharField(verbose_name='mtr.sync:value', max_length=255)),
            ],
            options={
                'verbose_name': 'mtr.sync:filter',
                'ordering': ('position',),
                'verbose_name_plural': 'mtr.sync:filters',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.PositiveSmallIntegerField(verbose_name='mtr.sync:action', choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], db_index=True)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', upload_to=mtr.sync.settings.get_buffer_file_path, blank=True, db_index=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='mtr.sync:status', default=1, choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')])),
                ('started_at', models.DateTimeField(verbose_name='mtr.sync:started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(verbose_name='mtr.sync:completed at', null=True, blank=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
            ],
            options={
                'verbose_name': 'mtr.sync:report',
                'ordering': ('-id',),
                'verbose_name_plural': 'mtr.sync:reports',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.PositiveSmallIntegerField(verbose_name='mtr.sync:action', choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], db_index=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=100, blank=True)),
                ('start_col', models.CharField(verbose_name='mtr.sync:start column', max_length=10, blank=True)),
                ('start_row', models.PositiveIntegerField(verbose_name='mtr.sync:start row', null=True, blank=True)),
                ('end_col', models.CharField(verbose_name='mtr.sync:end column', max_length=10, blank=True)),
                ('end_row', models.PositiveIntegerField(verbose_name='mtr.sync:end row', null=True, blank=True)),
                ('model', models.CharField(verbose_name='mtr.sync:model', max_length=255, blank=True, choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Settings'), ('mtr_sync.field', 'Mtr_Sync | Field'), ('mtr_sync.filter', 'Mtr_Sync | Filter'), ('mtr_sync.report', 'Mtr_Sync | Report'), ('mtr_sync.error', 'Mtr_Sync | Error')])),
                ('created_at', models.DateTimeField(verbose_name='mtr.sync:created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
                ('processor', models.CharField(verbose_name='mtr.sync:format', max_length=255, choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')])),
                ('worksheet', models.CharField(verbose_name='mtr.sync:worksheet page', max_length=255, blank=True)),
                ('include_header', models.BooleanField(verbose_name='mtr.sync:include header', default=True)),
                ('filename', models.CharField(verbose_name='mtr.sync:custom filename', max_length=255, blank=True)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', upload_to=mtr.sync.settings.get_buffer_file_path, blank=True, db_index=True)),
                ('dataset', models.CharField(verbose_name='mtr.sync:dataset', max_length=255, blank=True, choices=[('some_dataset', 'some description')])),
                ('filter_dataset', models.BooleanField(verbose_name='mtr.sync:filter custom dataset', default=True)),
                ('data_action', models.CharField(verbose_name='mtr.sync:data action', max_length=255, blank=True, choices=[('create', 'mtr.sync:Create instances without filter')])),
                ('language', models.CharField(verbose_name='mtr.sync:language', max_length=255, blank=True, choices=[('de', 'German'), ('en', 'English')])),
                ('language_attributes', models.BooleanField(verbose_name='mtr.sync:Hide translation prefixed fields', default=True)),
                ('create_fields', models.BooleanField(verbose_name='mtr.sync:Create settings for fields', default=True)),
                ('populate_from_file', models.BooleanField(verbose_name='mtr.sync:Populate settings from file', default=False)),
            ],
            options={
                'verbose_name': 'mtr.sync:settings',
                'ordering': ('-id',),
                'verbose_name_plural': 'mtr.sync:settings',
            },
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(blank=True, to='mtr_sync.Settings', verbose_name='mtr.sync:settings', null=True, related_name='reports'),
        ),
        migrations.AddField(
            model_name='filter',
            name='settings',
            field=models.ForeignKey(to='mtr_sync.Settings', verbose_name='mtr.sync:settings', related_name='filters'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(to='mtr_sync.Settings', verbose_name='mtr.sync:settings', related_name='fields'),
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(related_name='errors', to='mtr_sync.Report'),
        ),
    ]
